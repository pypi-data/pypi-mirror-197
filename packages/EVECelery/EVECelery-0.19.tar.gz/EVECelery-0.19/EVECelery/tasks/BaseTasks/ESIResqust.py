from EVECelery.exceptions.tasks import NotResolved, InputValidationError
from EVECelery.exceptions.utils import ErrorLimitExceeded
from EVECelery.utils.ErrorLimiter import ESIErrorLimiter
from EVECelery.utils.RequestHeaders import RequestHeaders
from redis import Redis
from celery.result import AsyncResult
import json
import requests
from datetime import datetime
from dateutil.parser import parse as dtparse
from .BaseTask import BaseTask


class ESIRequest(BaseTask):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = 5
    retry_backoff_max = 600
    retry_jitter = False

    def ttl_404(self) -> int:
        """Returns the redis TTL for caching ESI responses that errored with a 404 - not found

        :return: Seconds to cache a 404 not found ESI response in Redis
        :rtype: int
        """
        return 86400

    def get_key(self, **kwargs) -> str:
        """Returns the Redis key name for storing ESI responses

        :param kwargs: ESI request parameters
        :return: Redis key for storing the value of the ESI response
        :rtype: str
        """
        raise NotImplementedError

    def get_lock_key(self, **kwargs) -> str:
        """Returns the Redis key name for storing ESI locks

        :param kwargs: ESI request parameters
        :return: Redis key for storing ESI locks
        :rtype: str
        """
        k = self.get_key(**kwargs)
        return f"Lock-{k}"

    def base_url(self) -> str:
        """Base URL for ESI requests

        :return: ESI base request URL
        :rtype: str
        """
        return "https://esi.evetech.net/latest"

    def route(self, **kwargs) -> str:
        """ESI route with input request parameters

        :param kwargs: ESI request parameters to fill in the ESI request string
        :return: ESI route with request parameters
        :rtype: str
        """
        raise NotImplementedError

    def request_url(self, **kwargs) -> str:
        """ESI request URL with request parameters

        :param kwargs: ESI request parameters to fill in the ESI request string
        :return: ESI request URL with request parameters
        :rtype: str
        """
        return f"{self.base_url()}{self.route(**kwargs)}/?datasource=tranquility"

    def get_cached(self, **kwargs):
        """Get the cached response from ESI immediately without invoking an ESI call.

        :param kwargs: ESI request parameters
        :return: Dictionary or list containing cached response from ESI.
            If ESI returned a 404 error dictionary the response will be in the form
            {"error": error_message, "error_code": 404}
            Only /universe/factions/ and /markets/prices/ returns a list, all else return dictionaries.
        :rtype: dict or list
        :raises EVECelery.exceptions.ESI.NotResolved: If the request has not yet been resolved by ESI.
        :raises EVECelery.exceptions.ESI.InputValidationError: If an input ESI parameter contains
            invalid syntax or is a known invalid ID
        """
        self.validate_inputs(**kwargs)
        cached_data = self.redis_cache.get(self.get_key(**kwargs))
        if cached_data:
            return json.loads(cached_data)
        else:
            raise NotResolved(f"Not resolved. ESI request parameters: {kwargs}")

    def get_async(self, ignore_result: bool = False, **kwargs) -> AsyncResult:
        """Returns an async result / promise representing the future evaluation of a task.
        This function does not block the calling process and returns immediately.

        :param ignore_result: Set false to store result in celery result backend, else ignore the result.
        :type ignore_result: bool
        :param kwargs: ESI request parameters
        :return: Promise for a future evaluation of a celery task
        :rtype: celery.result.AsyncResult
        """
        self.validate_inputs(**kwargs)
        return self.apply_async(ignore_result=ignore_result, kwargs=kwargs)

    def get_sync(self, timeout: float = 10, **kwargs):
        """Call a task and block until the result is set.

        :param timeout: The time in seconds to block waiting for the task to complete.
        Setting this to None blocks forever.
        :type timeout: float
        :param kwargs: ESI request parameters
        :return: Dictionary or list containing response from ESI.
            If ESI returned a 404 dictionary error the response will be in the form
            {"error": error_message, "error_code": 404}
            Only /universe/factions/ and /markets/prices/ returns a list, all else return dictionaries.
        :rtype: dict or list
        """
        return self.get_async(ignore_result=False, **kwargs).get(timeout=timeout, propagate=True)

    def run(self, *args, **kwargs):
        return self._request_esi(**kwargs)

    def _request_esi(self, **kwargs):
        """Gets the ESI cached response.
        If the response is not yet cached or hasn't been resolved then perform an ESI call caching the new response.

        This function should not be called outside of celery tasks and should only be invoked
        by the task function handling a lookup queue.

        :param redis: The redis client
        :param kwargs: ESI request parameters
        :return: Dictionary containing response from ESI.
            If ESI returned a 404 error the response will be in the form
            {"error": error_message, "error_code": 404}
            If the response doesn't require request inputs then list is usually returned (list factions, prices, etc).
            If the response requires inputs a dictionary is usually returned.
            Only /universe/factions/ and /markets/prices/ returns a list, all else return dictionaries.
        :rtype: dict or list
        :raises EVECelery.exceptions.utils.ErrorLimitExceeded: If the remaining error limit is below the allowed threshold.
        """
        lookup_key = self.get_key(**kwargs)
        lock_key = self.get_lock_key(**kwargs)
        with self.redis_cache.lock(lock_key, blocking_timeout=15, timeout=300):
            try:
                return self.get_cached(**kwargs)
            except NotResolved:
                pass
            ESIErrorLimiter.check_limit(self.redis_cache)
            rheaders = {}
            try:
                resp = requests.get(self.request_url(**kwargs), headers=RequestHeaders.get_headers(),
                                    timeout=5, verify=True)
                rheaders = resp.headers
                if resp.status_code == 200:
                    d = resp.json()
                    ttl_expire = int(max(
                        (dtparse(rheaders["expires"], ignoretz=True) - datetime.utcnow()).total_seconds(),
                        1)
                    )
                    self.redis_cache.set(name=lookup_key, value=json.dumps(d), ex=ttl_expire)
                    self._hook_after_esi_success(d)
                    ESIErrorLimiter.update_limit(self.redis_cache,
                                                 error_limit_remain=int(rheaders["x-esi-error-limit-remain"]),
                                                 error_limit_reset=int(rheaders["x-esi-error-limit-reset"]),
                                                 time=dtparse(rheaders["date"], ignoretz=True)
                                                 )
                    return json.loads(self.redis_cache.get(lookup_key))
                elif resp.status_code == 400 or resp.status_code == 404:
                    d = {"error": str(resp.json().get("error")), "error_code": resp.status_code}
                    self.redis_cache.set(name=lookup_key, value=json.dumps(d), ex=self.ttl_404())
                    ESIErrorLimiter.update_limit(self.redis_cache,
                                                 error_limit_remain=int(rheaders["x-esi-error-limit-remain"]),
                                                 error_limit_reset=int(rheaders["x-esi-error-limit-reset"]),
                                                 time=dtparse(rheaders["date"], ignoretz=True)
                                                 )
                    return json.loads(self.redis_cache.get(lookup_key))
                else:
                    resp.raise_for_status()
            except Exception as ex:
                try:
                    ESIErrorLimiter.update_limit(self.redis_cache,
                                                 error_limit_remain=int(rheaders["x-esi-error-limit-remain"]),
                                                 error_limit_reset=int(rheaders["x-esi-error-limit-reset"]),
                                                 time=dtparse(rheaders["date"], ignoretz=True)
                                                 )
                except KeyError:
                    ESIErrorLimiter.decrement_limit(self.redis_cache, datetime.utcnow())
                raise ex

    def _hook_after_esi_success(self, esi_response) -> None:
        """Code to run with esi_response data after there was a successful 200 response from ESI.
        For example: use this function to optionally queue up additional ESI calls for ids returned.

        :param esi_response: ESI response from an API call
        :type esi_response: dict or list
        :rtype: None
        """
        return

    def validate_inputs(self, **kwargs) -> None:
        """Run validation checks before submitting an ESI request or hitting the cache.

        :param kwargs: ESI request parameters
        :return: None
        :raises EVECelery.exceptions.ESI.InputValidationError: If an input ESI parameter contains
            invalid syntax or is a known invalid ID
        """
        raise NotImplementedError
