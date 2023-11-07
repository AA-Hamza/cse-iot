import paho.mqtt.client
import logging
import time


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logging.warn("Connected to MQTT Broker!")
    else:
        logging.error("Failed to connect, return code: " + rc)


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    logging.info("Subscribed to id: " + str(mid))


FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


def on_disconnect(client, userdata, rc, properties=None):
    logging.error("Disconnected with result code: " + str(rc))
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.warn("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)
        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.warn("%s. Reconnect failed. Retrying...", err)
        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.error("Reconnect failed after %s attempts. Exiting...",
                  reconnect_count)


def get_mqtt_client(config: dict) -> paho.mqtt.client.Client:
    '''
    This function expects a config dict containing at least 
    required fields: url, port, username and password
    optional: client_id, tls, transport
    '''
    client = paho.mqtt.client.Client(client_id=config.get("client_id", ""),
                                     transport=config.get("transport", "tcp"),
                                     protocol=paho.mqtt.client.MQTTv5)
    client.username_pw_set(config["username"], config["password"])

    client.connect(config["url"], config["port"])
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    # client.on_subscribe= on_subscribe
    logging.info("connected")

    return client
