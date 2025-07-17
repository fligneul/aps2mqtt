import unittest
from unittest.mock import MagicMock, patch, call
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
            mock_publish.assert_any_call(
                self.handler.client,
                "homeassistant/sensor/aps_123456789_power/config",
                unittest.mock.ANY,
                retain=True,
            )
            # Inverter online status
            mock_publish.assert_any_call(
                self.handler.client,
                "homeassistant/binary_sensor/aps_987654321_online/config",
                unittest.mock.ANY,
                retain=True,
            )
            # Panel 1 power
            mock_publish.assert_any_call(
                self.handler.client,
                "homeassistant/sensor/aps_987654321_panel_1_power/config",
                unittest.mock.ANY,
                retain=True,
            )

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

        # Check the parsed data
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/power"], "100")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/energy/today"], "200")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/energy/lifetime"], "300")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/online"], "True")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/signal"], "80")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/temperature"], "50")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/frequency"], "60")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/power"], "300")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/voltage"], "240")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/1/power"], "150")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/1/voltage"], "240")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/2/power"], "150")
        self.assertEqual(parsed_data["aps2mqtt/aps/123456789/987654321/2/voltage"], "240")


if __name__ == "__main__":
    unittest.main()
