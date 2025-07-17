"""Handle MQTT connection and data publishing"""

import logging
import time
import atexit
import json
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
        if self.mqtt_config.discovery_enabled:
            self.discovery_topic = self.mqtt_config.discovery.prefix + "/"
        self.client = None
        self.status_topic = self.topic_prefix + "aps/status"
        self.discovery_messages_sent = False

    def on_connect(self, client, userdata, flags, reason_code, properties):
        """Callback function on broker connection"""
        del userdata, flags, properties
        if reason_code == 0:
            _LOGGER.info("Connected to MQTT Broker!")
            self._publish(client, self.status_topic, "online", retain=True)
        else:
            _LOGGER.error("Failed to connect: %s", reason_code)

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        """Callback function on broker disconnection"""
        del client, userdata, flags, properties
        _LOGGER.info("Disconnected from MQTT Broker: %s", reason_code)

    def _publish(self, client, topic, msg, retain=False):
        # If mqtt_retain is True in config, all messages are retained.
        # Otherwise, only LWT uses retain.
        actual_retain = retain or self.mqtt_config.retain
        result = client.publish(topic, msg, retain=actual_retain)
        if result.rc == 0:
            _LOGGER.debug("Send `%s` to topic `%s` (retain=%s)", msg, topic, actual_retain)
        else:
            _LOGGER.error("Failed to send message to topic %s: %s", topic, result.rc)

    def connect_mqtt(self):
        """Create connection to MQTT broker"""
        _LOGGER.debug("Create MQTT client")
        self.client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION2, self.mqtt_config.client_id
        )

        if len(self.mqtt_config.broker_user.strip()) > 0:
            _LOGGER.debug("Connect with user '%s'", self.mqtt_config.broker_user)
            self.client.username_pw_set(
                self.mqtt_config.broker_user, self.mqtt_config.broker_passwd
            )
        else:
            _LOGGER.debug("Connect anonymously")

        if self.mqtt_config.secured_connection:
            _LOGGER.debug("Use secured connection")
            if self.mqtt_config.cacerts_path is None:
                _LOGGER.warning("No ca_certs defined, using default one")

            self.client.tls_set(
                ca_certs=(
                    self.mqtt_config.cacerts_path
                    if self.mqtt_config.cacerts_path is not None
                    else certifi.where()
                )
            )
        else:
            _LOGGER.debug("Use unsecured connection")

        _LOGGER.debug("Set LWT on topic '%s'", self.status_topic)
        self.client.will_set(self.status_topic, "offline", qos=1, retain=True)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        _LOGGER.info(
            "Connect to broker '%s' on port %s",
            self.mqtt_config.broker_addr,
            self.mqtt_config.broker_port,
        )
        self.client.connect_async(self.mqtt_config.broker_addr, self.mqtt_config.broker_port)
        self.client.loop_start()
        atexit.register(self.disconnect)

    def disconnect(self):
        if self.client.is_connected():
            _LOGGER.info("Publishing 'offline' status on graceful exit.")
            self._publish(self.client, self.status_topic, "offline", retain=True)
        self.client.loop_stop()

    def publish_discovery_messages(self, data):
        """Publish discovery messages for all sensors"""
        if not self.mqtt_config.discovery_enabled or self.discovery_messages_sent:
            return

        ecu_id = data["ecu_id"]
        topic_base = self.topic_prefix + "aps/" + str(ecu_id)
        ecu_device = self._get_device_payload(ecu_id, "ECU")

        # ECU sensors
        self._publish_discovery_payload(
            "sensor",
            ecu_id,
            "power",
            ecu_device,
            topic_base,
            "current_power",
            "ECU Power",
            "power",
            "W",
            "mdi:solar-power",
        )
        self._publish_discovery_payload(
            "sensor",
            ecu_id,
            "today_energy",
            ecu_device,
            topic_base,
            "today_energy",
            "ECU Today Energy",
            "energy",
            "kWh",
            "mdi:solar-power",
        )
        self._publish_discovery_payload(
            "sensor",
            ecu_id,
            "lifetime_energy",
            ecu_device,
            topic_base,
            "lifetime_energy",
            "ECU Lifetime Energy",
            "energy",
            "kWh",
            "mdi:solar-power",
        )

        # Inverter sensors
        for inverter in data["inverters"]:
            inv_uid = inverter["uid"]
            inv_topic_base = topic_base + "/" + str(inv_uid)
            inv_device = self._get_device_payload(inv_uid, "Inverter", via_device=ecu_id)

            self._publish_discovery_payload(
                "binary_sensor",
                inv_uid,
                "online",
                inv_device,
                inv_topic_base,
                "online",
                "Inverter Online",
                None,
                None,
                "mdi:power-plug",
            )
            self._publish_discovery_payload(
                "sensor",
                inv_uid,
                "signal",
                inv_device,
                inv_topic_base,
                "signal",
                "Inverter Signal",
                "signal_strength",
                "dBm",
                "mdi:wifi",
            )
            self._publish_discovery_payload(
                "sensor",
                inv_uid,
                "temperature",
                inv_device,
                inv_topic_base,
                "temperature",
                "Inverter Temperature",
                "temperature",
                "°C",
                "mdi:thermometer",
            )
            self._publish_discovery_payload(
                "sensor",
                inv_uid,
                "frequency",
                inv_device,
                inv_topic_base,
                "frequency",
                "Inverter Frequency",
                "frequency",
                "Hz",
                "mdi:sine-wave",
            )
            self._publish_discovery_payload(
                "sensor",
                inv_uid,
                "power",
                inv_device,
                inv_topic_base,
                "power",
                "Inverter Power",
                "power",
                "W",
                "mdi:solar-power",
            )
            self._publish_discovery_payload(
                "sensor",
                inv_uid,
                "voltage",
                inv_device,
                inv_topic_base,
                "voltage",
                "Inverter Voltage",
                "voltage",
                "V",
                "mdi:lightning-bolt",
            )

            # Panel sensors
            for i, panel_power in enumerate(inverter.get("power", [])):
                panel_num = i + 1
                self._publish_discovery_payload(
                    "sensor",
                    inv_uid,
                    f"panel_{panel_num}_power",
                    inv_device,
                    inv_topic_base + f"/{panel_num}",
                    "power",
                    f"Panel {panel_num} Power",
                    "power",
                    "W",
                    "mdi:solar-panel",
                )

            for i, panel_voltage in enumerate(inverter.get("voltage", [])):
                panel_num = i + 1
                self._publish_discovery_payload(
                    "sensor",
                    inv_uid,
                    f"panel_{panel_num}_voltage",
                    inv_device,
                    inv_topic_base + f"/{panel_num}",
                    "voltage",
                    f"Panel {panel_num} Voltage",
                    "voltage",
                    "V",
                    "mdi:lightning-bolt",
                )

        self.discovery_messages_sent = True

    def _get_device_payload(self, device_id, device_name, via_device=None):
        payload = {
            "identifiers": [str(device_id)],
            "name": f"APS {device_name} {device_id}",
            "manufacturer": "APsystems",
        }
        if via_device:
            payload["via_device"] = str(via_device)
        return payload

    def _publish_discovery_payload(
        self,
        component,
        device_id,
        object_id,
        device_payload,
        state_topic_base,
        value_key,
        name,
        device_class,
        unit,
        icon,
    ):
        discovery_topic = f"{self.discovery_topic}{component}/aps_{device_id}_{object_id}/config"
        payload = {
            "name": name,
            "unique_id": f"aps_{device_id}_{object_id}",
            "state_topic": state_topic_base,
            "value_template": f"{{{{ value_json.{value_key} }}}}",
            "device": device_payload,
            "availability_topic": self.status_topic,
            "payload_available": "online",
            "payload_not_available": "offline",
        }
        if component == "binary_sensor":
            payload["payload_on"] = "true"
            payload["payload_off"] = "false"
        if device_class:
            payload["device_class"] = device_class
        if unit:
            payload["unit_of_measurement"] = unit
        if icon:
            payload["icon"] = icon

        self._publish(self.client, discovery_topic, json.dumps(payload), retain=True)

    def publish_values(self, data):
        """Publish ECU data to MQTT"""
        _LOGGER.debug("Start MQTT publish")

        retry_count = 0
        while (self.client is None or not self.client.is_connected()) and retry_count < _MAX_RETRY:
            _LOGGER.info("MQTT client not connected...")
            retry_count += 1
            time.sleep(5)

        if retry_count == _MAX_RETRY:
            _LOGGER.warning("MQTT values not published")
            raise ConnectionError("Can't connect to broker")

        self.publish_discovery_messages(data)

        for topic, value in self._parse_data(data).items():
            self._publish(self.client, topic, value)
        _LOGGER.debug("MQTT values published")

    def _parse_data(self, data):
        output = {}
        ecu_id = data["ecu_id"]
        ecu_topic_base = self.topic_prefix + "aps/" + str(ecu_id)
        ecu_payload = {
            "current_power": data["current_power"],
            "today_energy": data["today_energy"],
            "lifetime_energy": data["lifetime_energy"],
        }
        output[ecu_topic_base] = json.dumps(ecu_payload)

        for inverter in data["inverters"]:
            inverter_uid = str(inverter["uid"])
            inverter_topic_base = ecu_topic_base + "/" + inverter_uid
            inverter_payload = {
                "online": inverter["online"],
            }
            if inverter["online"]:
                inverter_payload["signal"] = inverter["signal"]
                inverter_payload["temperature"] = inverter["temperature"]
                inverter_payload["frequency"] = inverter["frequency"]
                inverter_payload["power"] = sum(inverter["power"])
                inverter_payload["voltage"] = mean(inverter["voltage"])

                for panel_index, panel_power in enumerate(inverter["power"], start=1):
                    inverter_payload[f"panel_{panel_index}_power"] = panel_power

                for panel_index, panel_voltage in enumerate(inverter["voltage"], start=1):
                    inverter_payload[f"panel_{panel_index}_voltage"] = panel_voltage

            output[inverter_topic_base] = json.dumps(inverter_payload)

        return output
