import unittest
from unittest.mock import patch, MagicMock, call
from aps2mqtt.apsystems.APSystemsSocket import APSystemsSocket, APSystemsInvalidData

class TestAPSystemsSocket(unittest.TestCase):

    def setUp(self):
        self.socket = APSystemsSocket("127.0.0.1")

    @patch.object(APSystemsSocket, 'aps_str')
    @patch.object(APSystemsSocket, 'aps_int')
    @patch.object(APSystemsSocket, 'aps_double')
    @patch.object(APSystemsSocket, 'check_ecu_checksum')
    def test_process_ecu_data(self, mock_check_checksum, mock_aps_double, mock_aps_int, mock_aps_str):
        # Arrange
        self.socket.ecu_raw_data = b'dummy_data' # Raw data won't be parsed directly
        mock_aps_str.side_effect = ["0001", "123456789012", "01", "003", "v1.0.0", "004", "tz01"]
        mock_aps_double.side_effect = [10.0, 20.0, 30.0]
        mock_aps_int.side_effect = [2, 3, 100, 100]

        # Act
        self.socket.process_ecu_data()

        # Assert
        self.assertEqual(self.socket.ecu_id, "123456789012")
        self.assertEqual(self.socket.lifetime_energy, 10.0 / 10)
        self.assertEqual(self.socket.current_power, 20.0)
        self.assertEqual(self.socket.today_energy, 30.0 / 100)
        self.assertEqual(self.socket.qty_of_inverters, 2)
        self.assertEqual(self.socket.qty_of_online_inverters, 3)
        mock_check_checksum.assert_called_once_with(b'dummy_data', "ECU Query")

    @patch.object(APSystemsSocket, 'aps_str')
    @patch.object(APSystemsSocket, 'aps_int')
    @patch.object(APSystemsSocket, 'aps_double')
    @patch.object(APSystemsSocket, 'aps_uid')
    @patch.object(APSystemsSocket, 'aps_short')
    @patch.object(APSystemsSocket, 'aps_timestamp')
    @patch.object(APSystemsSocket, 'check_ecu_checksum')
    @patch.object(APSystemsSocket, 'process_signal_data')
    def test_process_inverter_data(self, mock_process_signal_data, mock_check_checksum, mock_aps_timestamp, mock_aps_short, mock_aps_uid, mock_aps_double, mock_aps_int, mock_aps_str):
        # Arrange
        self.socket.inverter_raw_data = b'dummy_data'
        self.socket.qty_of_inverters = 1
        mock_aps_str.side_effect = ["0002", "00", "01", "01"]
        mock_aps_int.side_effect = [1, 600, 200, 150, 240, 150, 240]
        mock_aps_uid.return_value = "123456789012"
        mock_aps_short.return_value = 1
        mock_aps_timestamp.return_value = "2025-07-20 12:00:00"
        mock_process_signal_data.return_value = {"123456789012": 80}

        # Act
        data = self.socket.process_inverter_data()

        # Assert
        self.assertIn("inverters", data)
        self.assertEqual(len(data["inverters"]), 1)
        inverter = data["inverters"][0]
        self.assertEqual(inverter["uid"], "123456789012")
        self.assertTrue(inverter["online"])
        self.assertEqual(inverter["signal"], 80)
        self.assertEqual(inverter["frequency"], 60.0)
        self.assertEqual(inverter["temperature"], 100)
        mock_check_checksum.assert_called_once_with(b'dummy_data', "Inverter data")

    def test_check_ecu_checksum_invalid(self):
        with self.assertRaises(APSystemsInvalidData):
            self.socket.check_ecu_checksum(b'APS1100160001', "test")

    @patch.object(APSystemsSocket, 'open_socket')
    @patch.object(APSystemsSocket, 'close_socket')
    @patch.object(APSystemsSocket, 'send_read_from_socket')
    @patch.object(APSystemsSocket, 'process_ecu_data')
    @patch.object(APSystemsSocket, 'process_inverter_data')
    def test_query_ecu_success(self, mock_process_inverter_data, mock_process_ecu_data, mock_send_read_from_socket, mock_close_socket, mock_open_socket):
        # Arrange
        self.socket.ecu_id = "123456789012" # Set ecu_id for inverter queries
        self.socket.lifetime_energy = 100 # Set a non-zero lifetime_energy
        mock_send_read_from_socket.side_effect = [b'ecu_response', b'inverter_response', b'signal_response']
        mock_process_ecu_data.return_value = None # This method modifies self attributes
        mock_process_inverter_data.return_value = {"inverters": []}

        # Act
        data = self.socket.query_ecu()

        # Assert
        mock_open_socket.call_count == 3
        mock_close_socket.call_count == 3
        mock_send_read_from_socket.assert_has_calls([
            call(self.socket.ecu_query),
            call(self.socket.inverter_query_prefix + self.socket.ecu_id + self.socket.inverter_query_suffix),
            call(self.socket.inverter_signal_prefix + self.socket.ecu_id + self.socket.inverter_signal_suffix)
        ])
        mock_process_ecu_data.assert_called_once()
        mock_process_inverter_data.assert_called_once()
        self.assertIn("ecu_id", data)

if __name__ == '__main__':
    unittest.main()
