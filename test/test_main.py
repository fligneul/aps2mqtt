import unittest
from unittest.mock import patch, MagicMock
from aps2mqtt.main import main


class TestMain(unittest.TestCase):

    @patch("aps2mqtt.main.Config")
    @patch("aps2mqtt.main.MQTTHandler")
    @patch("aps2mqtt.apsystems.ECU.APSystemsSocket")
    def test_main(self, mock_apsystems_socket, mock_mqtt_handler, mock_config):
        # Mock the config object
        mock_config.return_value.ecu_config.ipaddr = "127.0.0.1"
        mock_config.return_value.ecu_config.port = 8899
        mock_config.return_value.ecu_config.auto_restart = False
        mock_config.return_value.ecu_config.stop_at_night = False
        mock_config.return_value.ecu_config.timezone = None
        mock_config.return_value.mqtt_config.discovery_enabled = False

        # Mock the MQTT handler
        mock_mqtt_instance = MagicMock()
        mock_mqtt_handler.return_value = mock_mqtt_instance

        # Mock the APSystems socket
        mock_aps_instance = MagicMock()
        mock_apsystems_socket.return_value = mock_aps_instance
        mock_aps_instance.query_ecu.return_value = {
            "ecu_id": "123456789",
            "timestamp": "2025-07-17 10:30:00",
            "current_power": 100,
            "today_energy": 200,
            "lifetime_energy": 300,
            "inverters": []
        }

        # Run the main function
        with patch("aps2mqtt.main.time.sleep", side_effect=InterruptedError):
            with self.assertRaises(InterruptedError):
                main()

        # Assert that the connect_mqtt method was called
        mock_mqtt_instance.connect_mqtt.assert_called_once()

        # Assert that the query_ecu method was called
        mock_aps_instance.query_ecu.assert_called()

        # Assert that the publish_values method was called
        mock_mqtt_instance.publish_values.assert_called()


if __name__ == '__main__':
    unittest.main()