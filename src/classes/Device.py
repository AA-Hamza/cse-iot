import paho.mqtt.client
import asyncio
import json
import logging
from typing import Dict
from classes.Command import Command
from classes.Sensor import Sensor

from utils.mqtt_client import get_mqtt_client
from datetime import datetime


class Device:
    enabled: bool = True
    model: str
    commands: Dict[str, Command]
    sensors: Dict[str, Sensor]
    status_update_interval: float = 5
    loop = asyncio.get_event_loop()

    mqtt_client: paho.mqtt.client.Client
    mqtt_base_topic: str

    def __init__(
        self,
        mqtt_config: dict,
        model: str,
    ) -> None:
        logging.info("init device of model: " + model)
        self.model = model
        self.commands = {}
        self.sensors = {}

        # Init the mqtt client
        self.__init_mqtt_client(mqtt_config)

    def __init_mqtt_client(self, mqtt_config: dict):
        self.mqtt_base_topic = mqtt_config["base"]
        self.mqtt_client = get_mqtt_client(mqtt_config)

        ## The device is only subscribing to command topic
        self.mqtt_client.subscribe(self.mqtt_base_topic + "command")

        def on_message(client: paho.mqtt.client.Client, userdata,
                       msg: paho.mqtt.client.MQTTMessage):
            logging.info("Recieved msg: {message}, on topic: {topic}".format(
                message=msg.payload, topic=msg.topic))
            if msg.topic == self.mqtt_base_topic + "command":
                logging.info("got a new command")
                try:
                    payload = json.loads(msg.payload)
                    command_name = payload.get("name", None)
                    command = self.commands.get(command_name, None)
                    if (command == None):
                        feedback = {
                            "error":
                            "command {command} is not supported".format(
                                command=command_name)
                        }
                        client.publish(self.mqtt_base_topic + "feedback",
                                       payload=json.dumps(feedback),
                                       qos=1)
                    else:
                        result = command.execute(payload.get("data", None))
                        for topic_extenstion, payload in result.items():
                            client.publish(self.mqtt_base_topic +
                                           topic_extenstion,
                                           payload=json.dumps(payload),
                                           qos=1)

                except Exception as e:
                    logging.error(
                        "got error while parsing the command payload {payload}, err: {err}"
                        .format(payload=msg.payload, err=e))

        self.mqtt_client.on_message = on_message

    def stop_device(self):
        self.enabled = False
        self.mqtt_client.loop_stop()
        self.loop.stop()

    def start_device(self):
        self.enabled = True
        self.mqtt_client.loop_start()
        self.__mqtt_startup_messages()
        self.loop.create_task(self.__send_time_loop())
        self.loop.create_task(self.__start_sensors_polling())
        self.loop.run_forever()

    async def __send_time_loop(self):
        while True:
            if (not self.enabled):
                break
            self.mqtt_client.publish(topic=self.mqtt_base_topic + "time",
                                     payload=datetime.utcnow().isoformat(),
                                     qos=1,
                                     retain=True)
            await asyncio.sleep(self.status_update_interval)

    async def __start_sensors_polling(self):
        logging.info("Starting sensors polling")

        async def _handle(s):
            while self.enabled:
                data = await s.poll()
                for topic_extenstion, payload in data.items():
                    logging.info(f"publishing {topic_extenstion}, {payload}")
                    self.mqtt_client.publish(self.mqtt_base_topic +
                                             "sensors/" + topic_extenstion,
                                             payload=json.dumps(payload),
                                             qos=1)

        for sensor in self.sensors.values():
            self.loop.create_task(_handle(sensor))

    def register_command(self, c: Command):
        name = c.command_name()
        self.commands[name] = c

    def register_sensor(self, s: Sensor):
        name = s.sensor_name()
        self.sensors[name] = s

    def __mqtt_startup_messages(self):
        ## Register capabilities
        result = []
        for command in self.commands.values():
            result.append(command.mqtt_full_name())
        for sensor in self.sensors.values():
            result.append(sensor.mqtt_full_name())
        payload = json.dumps(result)
        self.mqtt_client.publish(topic=self.mqtt_base_topic + "capabilities",
                                 payload=payload,
                                 qos=1,
                                 retain=True)

        ## Register initial state of commands
        for command in self.commands.values():
            init_state = command.current_state()
            for topic_extenstion, payload in init_state.items():
                logging.info(f"publishing {topic_extenstion}, {payload}")
                self.mqtt_client.publish(self.mqtt_base_topic +
                                         topic_extenstion,
                                         payload=json.dumps(payload),
                                         qos=1,
                                         retain=True)

        ## Register device model
        self.mqtt_client.publish(self.mqtt_base_topic + "model",
                                 payload=self.model,
                                 qos=1,
                                 retain=True)
