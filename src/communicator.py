import requests
import threading

class RaspberryPiCommunicator:
    def __init__(self, pi_ip="192.168.137.86", port=5000):
        self.base_url = f"http://{pi_ip}:{port}"
        self.timeout = 2

    def activate_alarm(self):
        self._send_request("on", blocking=False)

    def deactivate_alarm(self):
        self._send_request("off", blocking=True)

    def _send_request(self, status, blocking=False):
        url = f"{self.base_url}/alarm"
        json_data = {"status": status}

        def task():
            try:
                requests.post(url, json=json_data, timeout=self.timeout)
                print(f"[Communicator] Signal '{status}' sent successfully.")
            except requests.exceptions.RequestException:
                print(f"[Communicator] Warning: Could not reach Raspberry Pi at {self.base_url}")

        if blocking:
            task()
        else:
            threading.Thread(target=task, daemon=True).start()