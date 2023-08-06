import io

import requests

from lprp_core.service import Service, optionally_syncronized


class HardwareSimulator(Service):
    def __init__(self, address: str, identity: str):
        self.address = address
        self.identity = identity

    @optionally_syncronized
    async def is_available(self) -> bool:
        response = requests.get(f"{self.address}/is_available")
        return response.json()["is_available"]

    @optionally_syncronized
    async def get_activator_is_triggered(self) -> bool:
        response = requests.get(f"{self.address}/{self.identity}/activator_is_triggered")
        return response.json()["is_triggered"]

    @optionally_syncronized
    async def update_activator_is_triggered(self, value: bool) -> None:
        response = requests.post(f"{self.address}/{self.identity}/activator_is_triggered", json={"is_triggered": value})
        return

    @optionally_syncronized
    async def get_camera_current_image(self) -> bytes:
        response = requests.get(f"{self.address}/{self.identity}/camera_current_image")
        return io.BytesIO(response.content).read()

    @optionally_syncronized
    async def update_camera_current_image(self, value: bytes) -> None:
        response = requests.post(f"{self.address}/{self.identity}/camera_current_image", files={"image": value})
        return

    @optionally_syncronized
    async def get_gate_state(self) -> int:
        # TODO think about shared implementation of OutputState
        response = requests.get(f"{self.address}/{self.identity}/gate_state")
        return response.json()["gate_state"]

    @optionally_syncronized
    async def update_gate_state(self, value: int) -> None:
        response = requests.post(f"{self.address}/{self.identity}/gate_state", json={"gate_state": value})
        return

    @optionally_syncronized
    async def get_visual_indicator_state(self) -> int:
        # TODO think about shared implementation of OutputState
        response = requests.get(f"{self.address}/{self.identity}/visual_indicator_state")
        return response.json()["visual_indicator_state"]

    @optionally_syncronized
    async def update_visual_indicator_state(self, value: int) -> None:
        response = requests.post(f"{self.address}/{self.identity}/visual_indicator_state", json={"visual_indicator_state": value})
        return

