from lprp_core.service import Service, optionally_syncronized


class LicensePlateRecognition(Service):

    def __init__(self, address: str):
        pass

    @optionally_syncronized
    async def is_available(self) -> bool:
        raise NotImplementedError

    @optionally_syncronized
    async def get_license_plate(self, image: bytes) -> str:
        raise NotImplementedError
