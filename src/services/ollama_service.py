import socket
import subprocess
import time
from urllib.request import urlopen
from urllib.error import URLError


class OllamaService:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url.rstrip("/")
        self.process = None

    def is_running(self, timeout=1.5):
        try:
            with urlopen(f"{self.base_url}/api/tags", timeout=timeout) as response:
                return response.status == 200
        except (URLError, TimeoutError, OSError):
            return False

    def start(self):
        if self.is_running():
            return True
        try:
            self.process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except (FileNotFoundError, OSError):
            return False
        for _ in range(15):
            if self.is_running():
                return True
            time.sleep(0.3)
        return False
