from abc import ABC, abstractmethod

class Sensor(ABC):
    name: str
    state: dict

    def sensor_name(self) -> str:
        return self.name

    def mqtt_full_name(self) -> str:
        return "sensor." + self.name

    @abstractmethod
    async def poll(self) -> dict:
        pass
