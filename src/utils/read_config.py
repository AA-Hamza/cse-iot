import yaml

_MQTT_REQUIRED = ["url", "port", "username", "password", "base"]
_DEVICE_REQUIRED = ["model"]


def read_config(file_path: str = "./config.yaml"):
    '''
    example config.yaml

    mqtt:
        # Required
        url: mqtt.ahamza.live
        port: 8883
        username: pi
        password: somewhatstrongpassword
        base: devices/1/

        # Optional
        client_id: pi_home 
        tls: false
        clean_session: false
    '''
    with open(file_path, "r") as stream:
        obj: dict = yaml.safe_load((stream))
        if obj.get("mqtt", None) == None:
            raise Exception(
                f"can not find the mqtt section in the configuration file")
        else:
            device_config = obj["mqtt"]
            for value in _MQTT_REQUIRED:
                if (device_config.get(value, None) == None):
                    raise Exception(
                        "you need to provide mqtt.{field} in the config file".
                        format(field=value))

        if obj.get("device", None) == None:
            raise Exception(
                f"can not find the device section in the configuration file")
        else:
            device_config = obj.get("device", None)
            for value in _DEVICE_REQUIRED:
                if (device_config.get(value, None) == None):
                    raise Exception(
                        "you need to provide device.{field} in the config file".
                        format(field=value))
        return obj
