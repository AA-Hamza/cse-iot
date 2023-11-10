from classes.Command import Command


class SwitchCommand(Command):
    name: str = "virtual-switch"
    state: bool = False

    def execute(self, payload) -> dict:
        result = {}
        if (payload == "-"):
            self.state = not self.state
        elif (payload == "1"):
            self.state = True
        elif (payload == "0"):
            self.state = False
        else:
            result = {
                "feedback": {
                    "error":
                    self.mqtt_full_name() +
                    ", supported values are 0, 1 and - (string)"
                },
            }
            return result

        result = {
            "feedback": {
                "message":
                self.mqtt_full_name() +
                ", successfully changed the state to " + str(int(self.state))
            },
            self.name: str(int(self.state))
        }
        return result
