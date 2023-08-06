from enum import Enum

from lprp_core.service import Service, optionally_syncronized


class HealthStatus(Enum):
    HEALTHY = 0
    INCREASED_RISK = 1
    TEMPORARY_ISSUE = 2
    MAJOR_ISSUE = 3
    UNDEFINED = 4


class Healthcheck(Service):
    def __init__(self, address: str):
        pass

    @optionally_syncronized
    async def is_available(self) -> bool:
        raise NotImplementedError

    @optionally_syncronized
    async def get_health(self) -> HealthStatus:
        raise NotImplementedError

    @optionally_syncronized
    async def put_healthcheck(self, service_type: Service, address: str) -> int:
        raise NotImplementedError

    @optionally_syncronized
    async def delete_healthcheck(self, id: int) -> None:
        raise NotImplementedError
