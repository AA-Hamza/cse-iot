from classes import Device
from classes.commands.VirtualSwitch import SwitchCommand
from classes.sensors.VirtualDHT11 import VirtualHDHT11
from utils.read_config import read_config
import logging
import sys


def main():
    ## Logging
    logging.basicConfig(
        stream=sys.stdout,
        format=
        '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        level=logging.DEBUG)
    config = read_config()

    ## Virtual device
    virtual_device = Device.Device(config["mqtt"], "virtual")

    ## Virtual device virtual switcm
    virtual_switch = SwitchCommand()
    virtual_device.register_command(virtual_switch)

    ## Virtual device virtual sensor
    virtual_dht11 = VirtualHDHT11()
    virtual_device.register_sensor(virtual_dht11)

    try:
        virtual_device.start_device()
    except KeyboardInterrupt:
        print("stopping the device")
        virtual_device.stop_device()


if __name__ == "__main__":
    main()
