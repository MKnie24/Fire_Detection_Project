import unittest
from unittest.mock import patch
import time
from src.communicator import RaspberryPiCommunicator


class TestRaspberryPiCommunicator(unittest.TestCase):

    def setUp(self):
        self.comm = RaspberryPiCommunicator(pi_ip="192.168.1.50", port=5000)

    def test_initialization(self):
        expected_url = "http://192.168.1.50:5000"
        self.assertEqual(self.comm.base_url, expected_url)

    @patch('src.communicator.requests.post')
    def test_activate_alarm_sends_on(self, mock_post):
        self.comm.activate_alarm()

        time.sleep(0.1)

        mock_post.assert_called_with(
            "http://192.168.1.50:5000/alarm",
            json={"status": "on"},
            timeout=2
        )

    @patch('src.communicator.requests.post')
    def test_deactivate_alarm_sends_off(self, mock_post):
        self.comm.deactivate_alarm()

        time.sleep(0.1)

        mock_post.assert_called_with(
            "http://192.168.1.50:5000/alarm",
            json={"status": "off"},
            timeout=2
        )

    @patch('src.communicator.requests.post')
    def test_connection_error_is_handled(self, mock_post):
        mock_post.side_effect = Exception("Connection refused")

        try:
            self.comm.activate_alarm()
            time.sleep(0.1)
        except Exception:
            self.fail("Communicator shut down")