from abc import ABC, abstractmethod


class Command(ABC):
    name: str
    state: object

    def command_name(self) -> str:
        return self.name

    def mqtt_full_name(self) -> str:
        return "command." + self.name

    def current_state(self) -> dict:
        return {self.name: self.state}

    @abstractmethod
    def execute(self, payload) -> dict:
        pass
