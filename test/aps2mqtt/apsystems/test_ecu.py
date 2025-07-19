import logging
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from aps2mqtt.apsystems.ECU import ECU
from suntime import Sun


class TestECU(unittest.TestCase):

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")

    def setUp(self):
        # Create a mock for ecu_config
        self.ecu_config = MagicMock()
        self.ecu_config.stop_at_night = True
        self.ecu_config.ecu_position_latitude = 47.15276689916119
        self.ecu_config.ecu_position_longitude = -1.336921926016209

        # Create an instance of the ECU
        self.ecu = ECU(self.ecu_config)

    def test_should_sleep_when_stop_at_night_is_false(self):
        self.ecu.stop_at_night = False
        self.assertFalse(self.ecu.should_sleep())

    def test_should_sleep_when_cached_data_is_empty(self):
        self.ecu.cached_data = {}
        self.assertFalse(self.ecu.should_sleep())

    def test_should_sleep_when_inverters_are_online(self):
        self.ecu.cached_data = {"qty_of_online_inverters": 1}
        self.assertFalse(self.ecu.should_sleep())

    @patch("aps2mqtt.apsystems.ECU.datetime")
    def test_should_sleep_after_sunset(self, mock_datetime):
        # Arrange
        sun = Sun(self.ecu_config.ecu_position_latitude, self.ecu_config.ecu_position_longitude)
        sunset_time = sun.get_sunset_time()
        mock_datetime.now.return_value = sunset_time + timedelta(hours=1)

        self.ecu.cached_data = {"qty_of_online_inverters": 0}

        # Act & Assert
        self.assertTrue(self.ecu.should_sleep())

    @patch("aps2mqtt.apsystems.ECU.datetime")
    def test_should_sleep_before_sunrise(self, mock_datetime):
        # Arrange
        sun = Sun(self.ecu_config.ecu_position_latitude, self.ecu_config.ecu_position_longitude)
        sunrise_time = sun.get_sunrise_time()
        mock_datetime.now.return_value = sunrise_time - timedelta(hours=1)

        self.ecu.cached_data = {"qty_of_online_inverters": 0}

        # Act & Assert
        self.assertTrue(self.ecu.should_sleep())

    @patch("aps2mqtt.apsystems.ECU.datetime")
    def test_should_sleep_during_daytime(self, mock_datetime):
        # Arrange
        sun = Sun(self.ecu_config.ecu_position_latitude, self.ecu_config.ecu_position_longitude)
        sunrise_time = sun.get_sunrise_time()
        mock_datetime.now.return_value = sunrise_time + timedelta(hours=1)

        self.ecu.cached_data = {"qty_of_online_inverters": 0}

        # Act & Assert
        self.assertFalse(self.ecu.should_sleep())

    @patch("aps2mqtt.apsystems.ECU.datetime")
    def test_wake_up_time_before_sunrise(self, mock_datetime):
        # Arrange
        sun = Sun(self.ecu_config.ecu_position_latitude, self.ecu_config.ecu_position_longitude)
        sunrise_time = sun.get_sunrise_time()
        mock_datetime.now.return_value = sunrise_time - timedelta(hours=1)
        mock_datetime.today.return_value = mock_datetime.now.return_value.date()

        # Act
        wake_up = self.ecu.wake_up_time()

        # Assert
        self.assertEqual(wake_up.date(), sunrise_time.date())

    @patch("aps2mqtt.apsystems.ECU.datetime")
    def test_wake_up_time_after_sunrise(self, mock_datetime):
        # Arrange
        sun = Sun(self.ecu_config.ecu_position_latitude, self.ecu_config.ecu_position_longitude)
        sunrise_time = sun.get_sunrise_time()
        mock_datetime.now.return_value = sunrise_time + timedelta(hours=1)
        mock_datetime.today.return_value = mock_datetime.now.return_value.date()
        mock_datetime.side_effect = lambda *args, **kwargs: (
            datetime(*args, **kwargs) if len(args) > 0 else sunrise_time + timedelta(hours=1)
        )

        # Act
        wake_up = self.ecu.wake_up_time()

        # Assert
        self.assertEqual(wake_up.date(), (sunrise_time + timedelta(days=1)).date())


if __name__ == "__main__":
    unittest.main()
