import unittest
from unittest.mock import patch, mock_open
import os
import yaml
from aps2mqtt.config import MQTTConfig, ECUConfig, WifiConfig, Config

class TestConfig(unittest.TestCase):

    def test_mqtt_config_from_env(self):
        with patch.dict(os.environ, {
            "MQTT_BROKER_HOST": "mqtt.example.com",
            "MQTT_BROKER_PORT": "1884",
            "MQTT_BROKER_USER": "user",
            "MQTT_BROKER_PASSWD": "password",
            "MQTT_CLIENT_ID": "test_client",
            "MQTT_TOPIC_PREFIX": "test/topic",
            "MQTT_RETAIN": "True",
            "MQTT_DISCOVERY_ENABLED": "True",
            "MQTT_DISCOVERY_PREFIX": "test_discovery",
            "MQTT_BROKER_SECURED_CONNECTION": "True",
            "MQTT_BROKER_CACERTS_PATH": "/path/to/ca.crt"
        }):
            cfg = MQTTConfig(os.environ)
            self.assertEqual(cfg.broker_addr, "mqtt.example.com")
            self.assertEqual(cfg.broker_port, 1884)
            self.assertEqual(cfg.broker_user, "user")
            self.assertEqual(cfg.broker_passwd, "password")
            self.assertEqual(cfg.client_id, "test_client")
            self.assertEqual(cfg.topic_prefix, "test/topic")
            self.assertTrue(cfg.retain)
            self.assertTrue(cfg.discovery_enabled)
            self.assertEqual(cfg.discovery.prefix, "test_discovery")
            self.assertTrue(cfg.secured_connection)
            self.assertEqual(cfg.cacerts_path, "/path/to/ca.crt")

    def test_ecu_config_from_env(self):
        with patch.dict(os.environ, {
            "APS_ECU_IP": "192.168.1.100",
            "APS_ECU_PORT": "8888",
            "APS_ECU_TIMEZONE": "America/New_York",
            "APS_ECU_AUTO_RESTART": "True",
            "APS_ECU_WIFI_SSID": "my_wifi",
            "APS_ECU_WIFI_PASSWD": "wifi_password",
            "APS_ECU_STOP_AT_NIGHT": "True",
            "APS_ECU_POSITION_LAT": "40.7128",
            "APS_ECU_POSITION_LNG": "-74.0060"
        }):
            cfg = ECUConfig(os.environ)
            self.assertEqual(cfg.ipaddr, "192.168.1.100")
            self.assertEqual(cfg.port, 8888)
            self.assertEqual(str(cfg.timezone), "America/New_York")
            self.assertTrue(cfg.auto_restart)
            self.assertEqual(cfg.wifi_config.ssid, "my_wifi")
            self.assertEqual(cfg.wifi_config.passwd, "wifi_password")
            self.assertTrue(cfg.stop_at_night)
            self.assertEqual(cfg.ecu_position_latitude, 40.7128)
            self.assertEqual(cfg.ecu_position_longitude, -74.0060)

    def test_config_from_yaml(self):
        yaml_content = """
        mqtt:
          MQTT_BROKER_HOST: yaml.broker
          MQTT_BROKER_PORT: 1885
        ecu:
          APS_ECU_IP: 192.168.1.200
        """
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            with patch.object(yaml, 'safe_load', return_value=yaml.safe_load(yaml_content)):
                cfg = Config(config_path="dummy_path.yaml")
                self.assertEqual(cfg.mqtt_config.broker_addr, "yaml.broker")
                self.assertEqual(cfg.mqtt_config.broker_port, 1885)
                self.assertEqual(cfg.ecu_config.ipaddr, "192.168.1.200")

if __name__ == '__main__':
    unittest.main()
