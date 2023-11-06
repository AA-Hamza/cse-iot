from classes.Command import Command


class SwitchCommand(Command):
    name = "virtual-switch"
    state = False

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
                    self.mqtt_full_name() + ", supported values are 0, 1 and - (string)"
                },
            }

        if (result == {}):
            result = {
                "feedback": {
                    "message": self.mqtt_full_name() + ", successfully changed the"
                },
                "switch": "1" if self.state else "0"
            }
        return result
        # if (isinstance(payload, str)):
        # if (payload == "-"):
        #     self.state = not self.state
        # elif (payload == "1"):
        #     self.state = True
        # elif (payload == "0"):
        #     self.state = False
        # else:
        #     result = {
        #         "feedback": {
        #             "error": self.mqtt_full_name() + ", supported values are 0, 1 and -"
        #         },
        #     }
        #
        #
        # result = {
        #     "feedback": {
        #         "message": self.mqtt_full_name() + ", successfully changed the"
        #     },
        #     "switch": "1" if self.state else "0"
        # }
        # return result
        # if (isinstance(payload, str)):
        #     if (payload == "-"):
        #         self.state = not self.state
        #     elif (payload == "1"):
        #         self.state = True
        #     elif (payload == "0"):
        #         self.state = False
        #
        #     result = {
        #         "feedback": {
        #             "message":
        #             "successfully written {message} on lcd".format(
        #                 message=payload)
        #         },
        #         "switch": "1" if self.state else "0"
        #     }
        #     return result
