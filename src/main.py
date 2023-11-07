from classes import Device
from utils.read_config import read_config
import logging
import sys


def register_commands(device: Device.Device, commands_config: dict):
    for command in commands_config:
        command_name = command["name"]
        logging.info("Registering command: " + command_name)
        if (command_name == "virtual-switch"):
            from classes.commands.VirtualSwitch import SwitchCommand
            device.register_command(SwitchCommand())
            logging.info("Registered command: " + command_name + " successfully")
        elif (command_name == "lcd16x2"):
            from classes.commands.LCD16x2 import LCD16x2Command
            device.register_command(LCD16x2Command())
            logging.info("Registered command: " + command_name + " successfully")
        else:
            logging.error("command {command} is not implemented".format(command=command_name))

def register_sensors(device: Device.Device, sensors_config: dict):
    for sensor in sensors_config:
        sensor_name = sensor["name"]
        logging.info("Registering sensor: " + sensor_name)
        # if (sensor_name == "dht11"):
        if (sensor_name == "virtual-dht11"):
            from classes.sensors.VirtualDHT11 import VirtualDHT11
            device.register_sensor(VirtualDHT11())
            logging.info("Registered sensor: " + sensor_name + " successfully")
        else:
            logging.error("sensor {sensor} is not implemented".format(sensor=sensor_name))

def main():
    ## Logging
    logging.basicConfig(
        stream=sys.stdout,
        format=
        '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        level=logging.DEBUG)
    config = read_config()

    ## device
    device = Device.Device(config["mqtt"], config["device"]["model"])

    ## Register device commands
    if (config["device"].get("commands", None) != None):
        register_commands(device, config["device"]["commands"])

    ## Register device sensors
    if (config["device"].get("sensors", None) != None):
        register_sensors(device, config["device"]["sensors"])

    try:
        device.start_device()
    except KeyboardInterrupt:
        print("stopping the device")
        device.stop_device()


if __name__ == "__main__":
    main()
