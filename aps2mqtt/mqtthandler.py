"""Handle MQTT connection and data publishing"""
import logging
import time
import atexit
from statistics import mean
import certifi
from paho.mqtt import client as mqtt_client

_LOGGER = logging.getLogger(__name__)

_MAX_RETRY = 10


class MQTTHandler:
    """Handle MQTT connection to broker and publish message"""

    def __init__(self, mqtt_config):
        self.mqtt_config = mqtt_config
        self.topic_prefix = (
            mqtt_config.topic_prefix + "/" if len(mqtt_config.topic_prefix.strip()) > 0 else ""
        )
        self.client = None

    def on_connect(self, client, userdata, flags, rc):
        """Callback function on broker connection"""
        del client, userdata, flags
        if rc == 0:
            _LOGGER.info("Connected to MQTT Broker!")
        else:
            _LOGGER.error("Failed to connect: %s", mqtt_client.connack_string(rc))

    def on_disconnect(self, client, userdata, rc):
        """Callback function on broker disconnection"""
        del client, userdata
        _LOGGER.info("Disconnected from MQTT Broker: %s", mqtt_client.error_string(rc))

    def _publish(self, client, topic, msg):
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            _LOGGER.debug("Send `%s` to topic `%s`", msg, topic)
        else:
            _LOGGER.error(
                "Failed to send message to topic %s: %s", topic, mqtt_client.error_string(status)
            )

    def connect_mqtt(self):
        """Create connection to MQTT broker"""
        _LOGGER.debug("Create MQTT client")
        self.client = mqtt_client.Client(self.mqtt_config.client_id)

        if len(self.mqtt_config.broker_user.strip()) > 0:
            _LOGGER.debug("Connect with user '%s'", self.mqtt_config.broker_user)
            self.client.username_pw_set(
                self.mqtt_config.broker_user, self.mqtt_config.broker_passwd
            )
        else:
            _LOGGER.debug("Connect anonymously")

        if self.mqtt_config.secured_connection:
            _LOGGER.debug("Use secured connection")
            self.client.tls_set(
                ca_certs=(
                    self.mqtt_config.cacerts_path
                    if self.mqtt_config.cacerts_path is not None
                    else certifi.where()
                )
            )
        else:
            _LOGGER.debug("Use unsecured connection")

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        _LOGGER.info(
            "Connect to broker '%s' on port %s",
            self.mqtt_config.broker_addr,
            self.mqtt_config.broker_port,
        )
        self.client.connect_async(self.mqtt_config.broker_addr, self.mqtt_config.broker_port)
        self.client.loop_start()
        atexit.register(self.client.loop_stop)

    def publish_values(self, data):
        """Publish ECU data to MQTT"""
        _LOGGER.debug("Start MQTT publish")

        retry_count = 0
        while not self.client.is_connected() and retry_count < _MAX_RETRY:
            _LOGGER.info("MQTT client not connected...")
            retry_count += 1
            time.sleep(5)

        if retry_count == _MAX_RETRY:
            _LOGGER.warning("MQTT values not published")
            raise ConnectionError("Can't connect to broker")

        for topic, value in self._parse_data(data).items():
            self._publish(self.client, topic, value)
        _LOGGER.debug("MQTT values published")

    def _parse_data(self, data):
        output = {}
        ecu_id = data["ecu_id"]
        topic_base = self.topic_prefix + "aps/" + str(ecu_id)
        output[topic_base + "/power"] = str(data["current_power"])
        output[topic_base + "/energy/today"] = str(data["today_energy"])
        output[topic_base + "/energy/lifetime"] = str(data["lifetime_energy"])

        for inverter in data["inverters"]:
            topic_inv_base = topic_base + "/" + str(inverter["uid"])
            output[topic_inv_base + "/online"] = str(inverter["online"])
            if inverter["online"]:
                output[topic_inv_base + "/signal"] = str(inverter["signal"])
                output[topic_inv_base + "/temperature"] = str(inverter["temperature"])
                output[topic_inv_base + "/frequency"] = str(inverter["frequency"])
                output[topic_inv_base + "/power"] = str(sum(inverter["power"]))
                output[topic_inv_base + "/voltage"] = str(mean(inverter["voltage"]))

                for panel_index, panel_power in enumerate(inverter["power"], start=1):
                    output[topic_inv_base + "/" + str(panel_index) + "/power"] = str(panel_power)

                for panel_index, panel_voltage in enumerate(inverter["voltage"], start=1):
                    output[topic_inv_base + "/" + str(panel_index) + "/voltage"] = str(
                        panel_voltage
                    )

        return output
