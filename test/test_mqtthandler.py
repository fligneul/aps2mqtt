"""Test MQTTHandler"""
import unittest
from aps2mqtt.mqtthandler import MQTTHandler
from aps2mqtt.config import MQTTConfig


class TestParsing(unittest.TestCase):
    def test_parsing(self):
        """
        Test that it can parse ECU data
        """

        input_data = {
            "ecu_id": "12345",
            "current_power": 0.8,
            "today_energy": 42,
            "lifetime_energy": 1234.5,
            "inverters": [
                {
                    "uid": "inv_1",
                    "online": True,
                    "signal": 1,
                    "temperature": 12,
                    "frequency": 49.9,
                    "power": [100, 50],
                    "voltage": [230, 228],
                },
                {"uid": "inv_2", "online": False},
            ],
        }
        config = MQTTConfig({"MQTT_TOPIC_PREFIX": "test-prefix"})
        handler = MQTTHandler(config)
        result = handler._parse_data(input_data)

        self.assertEqual(len(result), 14)
        self.assertEqual(result.get("test-prefix/aps/12345/power"), "0.8")
        self.assertEqual(result.get("test-prefix/aps/12345/energy/today"), "42")
        self.assertEqual(result.get("test-prefix/aps/12345/energy/lifetime"), "1234.5")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/online"), "True")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/signal"), "1")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/temperature"), "12")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/frequency"), "49.9")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/power"), "150")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/voltage"), "229")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/1/power"), "100")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/1/voltage"), "230")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/2/power"), "50")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_1/2/voltage"), "228")
        self.assertEqual(result.get("test-prefix/aps/12345/inv_2/online"), "False")
