# EVECelery
[![PyPI](https://img.shields.io/pypi/v/EVECelery)](https://pypi.org/project/EVECelery)
[![EVECelery](https://github.com/NatEVETools/EVECelery/actions/workflows/github-actions.yml/badge.svg)](https://github.com/NatEVETools/EVECelery/actions/workflows/github-actions.yml)

ESI API requests library using [RabbitMQ](https://www.rabbitmq.com/), [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) tasks queues, and [Redis](https://redis.io/) caching.

# Installation
```
pip install EVECelery
```

# Usage
## Starting the Celery worker server
### From CLI

Set the following environmental variables and then run EVECelery from the CLI.
Variables: BrokerUser, BrokerPassword, BrokerHost, BrokerPort, BrokerVhost, ResultBackendUser, ResultBackendPassword, ResultBackendHost, ResultBackendPort, ResultBackendDb

```shell
python EVECelery
```

### From your code
From your worker code start the Celery worker server that handles running tasks:

```python
from EVECelery.CeleryApps import CeleryWorker

c = CeleryWorker(broker_user="user", broker_password="pass", broker_host="host", broker_port=5672, broker_vhost="esi",
                 result_user="user", result_password="pass", result_host="host", result_port=6379, result_db=0,
                 header_email="youremail@example.com")

c.start(
    max_concurrency=10)  # Start celery app - equivalent to running "celery worker -l WARNING --autoscale 10,1 -Q queues"
```

## Using EVECelery in your code
From another Python script you can send tasks to the queues and receive results:

```python
from EVECelery.CeleryApps import CeleryWorker
from EVECelery.tasks.Universe import *

c = CeleryWorker(broker_user="user", broker_password="pass", broker_host="host", broker_port=5672, broker_vhost="esi",
                 result_user="user", result_password="pass", result_host="host", result_port=6379, result_db=0,
                 header_email="youremail@example.com")  # only need to call this once in our code to init the tasks
r = SystemInfo().get_sync(timeout=5, system_id=30000142)
print(r)
```

# Current supported endpoints

| ESI Route                                    | EVECelery Task        |
|----------------------------------------------|-----------------------|
| /alliances/{alliance_id}/                    | AllianceInfo()        |
| /characters/{character_id}/                  | CharacterPublicInfo() |
| /corporations/{corporation_id}/              | CorporationInfo()     |
| /markets/prices/                             | PricesList()          |
| /universe/categories/{category_id}/          | CategoryInfo()        |
| /universe/constellations/{constellation_id}/ | ConstellationInfo()   |
| /universe/factions/                          | FactionsList()        |
| /universe/groups/{group_id}/                 | GroupInfo()           |
| /universe/regions/{region_id}/               | RegionInfo()          |
| /universe/systems/{system_id}/               | SystemInfo()          |
| /universe/types/{type_id}/                   | TypeInfo()            |

# Examples

See the included example scripts under [docs/examples](https://github.com/NatEVETools/EVECelery/tree/main/docs/examples)

# Copyright Notice

See [CCP.md](https://github.com/NatEVETools/EVECelery/blob/main/CCP.md)

