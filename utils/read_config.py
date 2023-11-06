import yaml

_REQUIRED = ["url", "port", "username", "password", "base"]


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
        mqtt_config = obj.get("mqtt", None)
        if mqtt_config == None:
            raise Exception(
                f"can not find the mqtt section in the configuration file")
        for value in _REQUIRED:
            if (mqtt_config.get(value, None) == None):
                raise Exception(
                    "you need to provide mqtt.{field} in the config file".
                    format(field=value))
        return obj
