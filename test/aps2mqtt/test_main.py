import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from aps2mqtt.main import cli_args, main

class TestMain(unittest.TestCase):

    @patch('aps2mqtt.main.ArgumentParser')
    def test_cli_args(self, mock_parser):
        # Arrange
        mock_parser_instance = MagicMock()
        mock_parser.return_value = mock_parser_instance

        # Act
        cli_args()

        # Assert
        mock_parser_instance.add_argument.assert_any_call(
            "-c", "--config", dest="config_path", help="load YAML config file", metavar="FILE"
        )
        mock_parser_instance.add_argument.assert_any_call(
            "-D", "--debug", dest="debug_level", help="enable debug logs", action="store_true"
        )
        mock_parser_instance.parse_args.assert_called_once()

    @patch('aps2mqtt.main.Config')
    @patch('aps2mqtt.main.ECU')
    @patch('aps2mqtt.main.MQTTHandler')
    @patch('aps2mqtt.main.time.sleep', side_effect=InterruptedError)  # To break the loop
    @patch('aps2mqtt.main.datetime')
    @patch('aps2mqtt.main.cli_args')
    def test_main_loop(self, mock_cli_args, mock_datetime, mock_sleep, mock_mqtt, mock_ecu, mock_config):
        # Arrange
        mock_args = MagicMock()
        mock_args.config_path = None
        mock_args.debug_level = False
        mock_cli_args.return_value = mock_args

        mock_ecu_instance = MagicMock()
        mock_ecu.return_value = mock_ecu_instance
        mock_ecu_instance.should_sleep.return_value = False
        mock_ecu_instance.update.return_value = {"timestamp": "2025-07-20 12:00:00"}

        mock_mqtt_instance = MagicMock()
        mock_mqtt.return_value = mock_mqtt_instance

        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        mock_config_instance.ecu_config.timezone = ZoneInfo("UTC")

        # Mock datetime.now to control the loop
        mock_datetime.now.side_effect = [
            datetime(2025, 7, 20, 11, 59, 0, tzinfo=timezone.utc), # Before update_time
            datetime(2025, 7, 20, 12, 0, 1, tzinfo=timezone.utc), # After update_time, to trigger update
            datetime(2025, 7, 20, 12, 10, 0, tzinfo=timezone.utc)  # After next update_time
        ]
        mock_datetime.strptime.return_value = datetime(2025, 7, 20, 12, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if args else mock_datetime.now()

        # Act
        with self.assertRaises(InterruptedError):
            main()

        # Assert
        mock_ecu_instance.update.assert_called_once()
        mock_mqtt_instance.publish_values.assert_called_once()

if __name__ == '__main__':
    unittest.main()
