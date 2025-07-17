import unittest
from unittest.mock import MagicMock, patch, call
import json
from aps2mqtt.mqtthandler import MQTTHandler


class TestMQTTHandler(unittest.TestCase):

    def setUp(self):
        self.mock_mqtt_config = MagicMock()
        self.mock_mqtt_config.discovery_enabled = True
        self.mock_mqtt_config.discovery.prefix = "homeassistant"
        self.mock_mqtt_config.topic_prefix = "aps2mqtt"
        self.mock_mqtt_config.retain = False
        self.handler = MQTTHandler(self.mock_mqtt_config)
        self.handler.client = MagicMock()

    def test_publish_discovery_messages(self):
        data = {
            "ecu_id": "123456789",
            "current_power": 100,
            "today_energy": 200,
            "lifetime_energy": 300,
            "inverters": [
                {
                    "uid": "987654321",
                    "online": True,
                    "signal": 80,
                    "temperature": 50,
                    "frequency": 60,
                    "power": [150, 150],
                    "voltage": [240, 240],
                }
            ],
        }

        with patch.object(self.handler, "_publish") as mock_publish:
            self.handler.publish_discovery_messages(data)

            # Check that the discovery messages are published
            self.assertGreater(mock_publish.call_count, 0)

            # Check the content of a few discovery messages
            # ECU power
            args, kwargs = mock_publish.call_args_list[0]
            payload = json.loads(args[2])
            self.assertEqual(payload["state_topic"], "aps2mqtt/aps/123456789")
            self.assertEqual(payload["value_template"], "{{ value_json.current_power }}")
            self.assertEqual(payload["availability_topic"], "aps2mqtt/aps/status")
            self.assertEqual(payload["payload_available"], "online")
            self.assertEqual(payload["payload_not_available"], "offline")

            # Inverter online status
            args, kwargs = mock_publish.call_args_list[3]
            payload = json.loads(args[2])
            self.assertEqual(payload["state_topic"], "aps2mqtt/aps/123456789/987654321")
            self.assertEqual(payload["value_template"], "{{ value_json.online }}")
            self.assertEqual(payload["availability_topic"], "aps2mqtt/aps/status")
            self.assertEqual(payload["payload_available"], "online")
            self.assertEqual(payload["payload_not_available"], "offline")

            # Panel 1 power
            args, kwargs = mock_publish.call_args_list[9]
            payload = json.loads(args[2])
            self.assertEqual(payload["state_topic"], "aps2mqtt/aps/123456789/987654321/1")
            self.assertEqual(payload["value_template"], "{{ value_json.power }}")
            self.assertEqual(payload["availability_topic"], "aps2mqtt/aps/status")
            self.assertEqual(payload["payload_available"], "online")
            self.assertEqual(payload["payload_not_available"], "offline")

    def test_parse_data(self):
        data = {
            "ecu_id": "123456789",
            "current_power": 100,
            "today_energy": 200,
            "lifetime_energy": 300,
            "inverters": [
                {
                    "uid": "987654321",
                    "online": True,
                    "signal": 80,
                    "temperature": 50,
                    "frequency": 60,
                    "power": [150, 150],
                    "voltage": [240, 240],
                }
            ],
        }

        parsed_data = self.handler._parse_data(data)

        # Check the ECU data payload
        ecu_payload = json.loads(parsed_data["aps2mqtt/aps/123456789"])
        self.assertEqual(ecu_payload["current_power"], 100)
        self.assertEqual(ecu_payload["today_energy"], 200)
        self.assertEqual(ecu_payload["lifetime_energy"], 300)

        # Check the inverter data payload
        inverter_payload = json.loads(parsed_data["aps2mqtt/aps/123456789/987654321"])
        self.assertEqual(inverter_payload["online"], True)
        self.assertEqual(inverter_payload["signal"], 80)
        self.assertEqual(inverter_payload["temperature"], 50)
        self.assertEqual(inverter_payload["frequency"], 60)
        self.assertEqual(inverter_payload["power"], 300)
        self.assertEqual(inverter_payload["voltage"], 240.0)
        self.assertEqual(inverter_payload["panel_1_power"], 150)
        self.assertEqual(inverter_payload["panel_1_voltage"], 240)
        self.assertEqual(inverter_payload["panel_2_power"], 150)
        self.assertEqual(inverter_payload["panel_2_voltage"], 240)


if __name__ == "__main__":
    unittest.main()
