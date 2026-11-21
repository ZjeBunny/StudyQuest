from PySide6.QtCore import QObject, QThread, Signal
from ai.note import NoteAI


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
