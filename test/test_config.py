import unittest
from unittest.mock import patch
from aps2mqtt.config import Config, MQTTConfig, ECUConfig, MQTTDiscoveryConfig


class TestConfig(unittest.TestCase):

    def test_load_yaml_config_file(self):
        # Create a dummy yaml file
        with open("config.yaml", "w") as f:
            f.write("""mqtt:
  MQTT_BROKER_HOST: localhost
  MQTT_BROKER_PORT: 1883
  MQTT_DISCOVERY_ENABLED: True
  MQTT_DISCOVERY_PREFIX: homeassistant
ecu:
  APS_ECU_IP: 192.168.1.100
""")

        config = Config("config.yaml")
        self.assertIsInstance(config.mqtt_config, MQTTConfig)
        self.assertIsInstance(config.ecu_config, ECUConfig)
        self.assertEqual(config.mqtt_config.broker_addr, "localhost")
        self.assertEqual(config.mqtt_config.broker_port, 1883)
        self.assertTrue(config.mqtt_config.discovery_enabled)
        self.assertIsInstance(config.mqtt_config.discovery, MQTTDiscoveryConfig)
        self.assertEqual(config.mqtt_config.discovery.prefix, "homeassistant")
        self.assertEqual(config.ecu_config.ipaddr, "192.168.1.100")

    @patch.dict("os.environ", {
        "MQTT_BROKER_HOST": "mqtt.example.com",
        "MQTT_BROKER_PORT": "8883",
        "APS_ECU_IP": "192.168.1.200",
        "MQTT_DISCOVERY_ENABLED": "True",
        "MQTT_DISCOVERY_PREFIX": "test_prefix",
    })
    def test_load_env_variables(self):
        config = Config()
        self.assertIsInstance(config.mqtt_config, MQTTConfig)
        self.assertIsInstance(config.ecu_config, ECUConfig)
        self.assertEqual(config.mqtt_config.broker_addr, "mqtt.example.com")
        self.assertEqual(config.mqtt_config.broker_port, 8883)
        self.assertTrue(config.mqtt_config.discovery_enabled)
        self.assertIsInstance(config.mqtt_config.discovery, MQTTDiscoveryConfig)
        self.assertEqual(config.mqtt_config.discovery.prefix, "test_prefix")
        self.assertEqual(config.ecu_config.ipaddr, "192.168.1.200")


if __name__ == '__main__':
    unittest.main()