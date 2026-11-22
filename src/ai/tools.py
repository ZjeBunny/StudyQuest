from threading import Lock
from PySide6.QtCore import QObject, QThread, Signal
from ai.note import NoteAI


class AIGate(QObject):
    busy_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._lock = Lock()

    def claim(self):
        if not self._lock.acquire(blocking=False):
            return False
        self.busy_changed.emit(True)
        return True

    def release(self):
        if self._lock.locked():
            self._lock.release()
            self.busy_changed.emit(False)


ai_gate = AIGate()


class AIWorker(QThread):
    succeeded = Signal(object)
    failed = Signal(str)

    def __init__(self, operation, *args, parent=None, **kwargs):
        super().__init__(parent)
        self.operation = operation
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            ai = NoteAI(**self.kwargs)
            result = getattr(ai, self.operation)(*self.args)
            self.succeeded.emit(result)
        except Exception as error:
            self.failed.emit(str(error))
        finally:
            ai_gate.release()
