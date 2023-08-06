from celery import Celery, Task
from EVECelery.__version__ import __version__, __url__, __license__
from EVECelery.tasks.Alliance import *
from EVECelery.tasks.Character import *
from EVECelery.tasks.Corporation import *
from EVECelery.tasks.Market import *
from EVECelery.tasks.Routes import *
from EVECelery.tasks.Universe import *
from EVECelery.clients.ClientRabbitMQ import ClientRabbitMQ
from EVECelery.clients.ClientRedis import ClientRedisResultBackend
import os
from typing import Optional


class CeleryWorker(object):
    """Celery worker server wrapper.
    Creating an instance of this class creates a celery app and registers the default tasks.

    :param broker_user: RabbitMQ user
    :param broker_password: RabbitMQ password
    :param broker_host: RabbitMQ hostname
    :param broker_port: RabbitMQ port - normally 5672
    :param broker_vhost: RabbitMQ vhost - namespace for all EVECelery queues
    :param result_user: Redis user - normally "default" if not explicitly configured
    :param result_password: Redis password
    :param result_host: Redis hostname
    :param result_port: Redis port - normally 6379
    :param result_db: Redis db - normally 0 for the default db
    :param config_object: Custom config object to overwrite the default EVECelery.celeryconfig - optional
    :param esi_queue_prefix: Prefix to add to all generated ESI queue names
    """

    def __init__(self, broker_user: Optional[str] = None, broker_password: Optional[str] = None,
                 broker_host: Optional[str] = None, broker_port: Optional[int] = None,
                 broker_vhost: Optional[str] = None,
                 result_user: Optional[str] = None, result_password: Optional[str] = None,
                 result_host: Optional[str] = None, result_port: Optional[int] = None, result_db: Optional[int] = None,
                 config_object: str = "EVECelery.celeryconfig", esi_queue_prefix: str = "ESI-",
                 connection_check: bool = False):
        self.broker = ClientRabbitMQ(user=broker_user, password=broker_password, host=broker_host, port=broker_port,
                                     vhost=broker_vhost)
        self.result_backend = ClientRedisResultBackend(user=result_user, password=result_password, host=result_host,
                                                       port=result_port, db=result_db)

        if connection_check:
            self.result_backend.check_connection()

        self.max_concurrency = int(os.environ.get('EVECelery_MaxConcurrency', 4))

        self.esi_queue_prefix = esi_queue_prefix
        self.app = Celery("EVECelery")
        self.app.config_from_object(config_object)
        self.app.conf.update(broker_url=self.broker.connection_str)
        self.app.conf.update(result_backend=self.result_backend.connection_str)
        self.app.conf.update(task_default_queue=f"{self.esi_queue_prefix}Default")

        self.queues = [f"{self.esi_queue_prefix}Default"]
        self.task_routes = {}
        self.beat_schedule = {}
        self._register_defaults()

    def esi_tasks(self):
        """Default ESI tasks

        :return: ESI task instances registered by default
        """
        yield AllianceInfo()
        yield CharacterPublicInfo()
        yield CorporationInfo()
        yield PricesList()
        yield CategoryInfo()
        yield ConstellationInfo()
        yield FactionsList()
        yield GroupInfo()
        yield RegionInfo()
        yield Route()
        yield SystemInfo()
        yield TypeInfo()

    def tasks_to_register(self):
        """Yields tuple pairs of (task, queue name) to register with the Celery app

        :return: yields tuple consisting of (task instance, queue name)
        """
        for t in self.esi_tasks():
            yield (t, f"{self.esi_queue_prefix}{t.name}")

    def _register_defaults(self):
        for t in self.tasks_to_register():
            self.register_task(t[0])
            self.register_additional_queue(t[1])
            self.register_task_route(t[0].name, t[1])

    def register_additional_queue(self, queue: str):
        """Register an additional queue that this Celery app should process.

        :param queue: Name of the queue
        :return: None
        """
        self.queues.append(queue)

    def register_task_route(self, task_name: str, queue_name: str):
        """Register a task to a specific queue using a Celery task route.

        :param task_name: The name of the task
        :param queue_name: Name of the queue to route tasks to.
        :return: None
        """
        self.task_routes[task_name] = {"queue": queue_name}
        self.app.conf.update(task_routes=self.task_routes)

    def register_task(self, task: Task):
        """Register a task instance with the Celery app. A task must inherit from the Celery Task base class.

        :param task: A task instance
        :return: None
        """
        self.app.register_task(task)

    @classmethod
    def print_header(cls):
        print(f"EVECelery {__version__} ({__url__})\n{__license__}")

    def start(self):
        """Starts the Celery app and beings processing messages in the queues.

        :return: None
        """
        self.print_header()
        self.app.start(argv=["worker", "-l", "WARNING", f"--autoscale={self.max_concurrency},1",
                             "-Q", ",".join(self.queues)])


class CeleryBeat(CeleryWorker):
    """Celery beat scheduler for periodic tasks.

    """

    def schedule_task(self, schedule_name: str, schedule_config: dict):
        """Schedule a task to run at intervals. The passed in schedule object is a dictionary following the
        format and fields described here:
        https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#available-fields

        :param schedule_name: Name of the scheduled job. This must be unique.
        :param schedule_config: The scheduled job config as specified at
            https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#available-fields
        :return: None
        """
        self.beat_schedule[schedule_name] = schedule_config
        self.app.conf.update(beat_schedule=self.beat_schedule)

    def start(self):
        self.print_header()
        self.app.start(argv=["beat"])
