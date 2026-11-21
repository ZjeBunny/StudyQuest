
import json
from urllib.request import urlopen
from urllib.error import URLError

from PySide6.QtCore import QObject, QThread, QTimer, Signal, Slot


class AIStatusWorker(QObject):
    finished = Signal(bool, str)

    def __init__(self, base_url, model):
        super().__init__()

        self.base_url = base_url.rstrip("/")
        self.model = model

    @Slot()
    def check(self):
        try:
            with urlopen(
                f"{self.base_url}/api/tags",
                timeout=2
            ) as response:
                data = json.load(response)

            models = [
                item.get("name", "")
                for item in data.get("models", [])
            ]

            if self.model not in models:
                self.finished.emit(
                    False,
                    f"Brak modelu {self.model}"
                )
                return

            self.finished.emit(True, "AI Online")

        except (URLError, OSError, ValueError) as error:
            self.finished.emit(
                False,
                f"Ollama niedostępna: {error}"
            )


class AIStatusService(QObject):
    status_changed = Signal(bool, str)

    def __init__(
        self,
        base_url="http://localhost:11434",
        model="qwen3:4b",
        parent=None
    ):
        super().__init__(parent)

        self.base_url = base_url
        self.model = model

        self.thread = None
        self.worker = None

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.check_status)

    def start(self):
        self.timer.start()
        self.check_status()

    def stop(self):
        self.timer.stop()

    def check_status(self):
        if self.thread is not None:
            return

        thread = QThread(self)
        worker = AIStatusWorker(
            self.base_url,
            self.model
        )

        worker.moveToThread(thread)

        thread.started.connect(worker.check)

        worker.finished.connect(self.status_changed)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)

        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self.cleanup)

        self.thread = thread
        self.worker = worker

        thread.start()

    @Slot()
    def cleanup(self):
        self.thread = None
        self.worker = None
