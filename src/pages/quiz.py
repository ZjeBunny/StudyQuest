from html.parser import HTMLParser
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton,
    QButtonGroup, QMessageBox, QComboBox, QProgressBar, QStackedWidget,
    QFrame
)
from ai.tools import AIWorker, ai_gate
from services.progress import ProgressStore
from time import monotonic
from database.notes_repository import NotesRepository
from services.notes_storage import NotesStorage


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "div", "h1", "h2", "h3", "li", "br"):
            self.parts.append("\n")


class QuizPage(QWidget):
    page_requested = Signal(str)
    activity = Signal(str)

    def __init__(self, settings=None):
        super().__init__()
        self.setObjectName("QuizPage")
        self.settings = settings
        self.repository = NotesRepository()
        self.storage = NotesStorage()
        self.worker = None
        self.busy = False
        ai_gate.busy_changed.connect(self._ai_busy_changed)
        self.mode = None
        self.questions = []
        self.cards = []
        self.index = 0
        self.card_index = 0
        self.score = 0
        self.answered = False
        self.flipped = False

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(14)
        title = QLabel("Quizy i fiszki")
        title.setObjectName("PageTitle")
        root.addWidget(title)
        subtitle = QLabel("Wybierz rodzaj nauki, kategorię i źródłowe notatki. AI dobierze liczbę zadań.")
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        home = QWidget()
        home_layout = QVBoxLayout(home)
        home_layout.addStretch()
        buttons = QHBoxLayout()
        self.quiz_choice = QPushButton("📝\n\nQUIZY\n\nSprawdź swoją wiedzę")
        self.flash_choice = QPushButton("📚\n\nFISZKI\n\nPowtarzaj pojęcia")
        for button, mode in ((self.quiz_choice, "quiz"), (self.flash_choice, "cards")):
            button.setMinimumHeight(220)
            button.setMinimumWidth(230)
            button.setStyleSheet("font-size: 19px; font-weight: bold; border: 1px solid #829CC5; border-radius: 14px; padding: 24px;")
            button.clicked.connect(lambda checked=False, m=mode: self.choose_mode(m))
            buttons.addWidget(button)
        home_layout.addLayout(buttons)
        home_layout.addStretch()
        self.stack.addWidget(home)

        page = QWidget()
        content = QVBoxLayout(page)
        back = QPushButton("← Wybór trybu")
        back.clicked.connect(self.back_home)
        content.addWidget(back, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mode_title = QLabel()
        self.mode_title.setObjectName("SectionTitle")
        content.addWidget(self.mode_title)
        selectors = QHBoxLayout()
        self.category = QComboBox()
        self.category.currentIndexChanged.connect(self.refresh_sources)
        self.source = QComboBox()
        selectors.addWidget(QLabel("Kategoria:"))
        selectors.addWidget(self.category, 1)
        selectors.addWidget(QLabel("Materiał:"))
        selectors.addWidget(self.source, 2)
        content.addLayout(selectors)
        self.generate = QPushButton("Generuj automatycznie")
        self.generate.setObjectName("PrimaryButton")
        self.generate.clicked.connect(self.generate_material)
        content.addWidget(self.generate)
        self.status = QLabel("Wybierz materiał do nauki.")
        self.status.setWordWrap(True)
        content.addWidget(self.status)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        content.addWidget(self.progress)

        self.question = QLabel()
        self.question.setObjectName("SectionTitle")
        self.question.setWordWrap(True)
        content.addWidget(self.question)
        self.group = QButtonGroup(self)
        self.buttons = []
        for i in range(4):
            button = QRadioButton()
            button.setMinimumHeight(44)
            self.group.addButton(button, i)
            self.buttons.append(button)
            content.addWidget(button)
            button.hide()
        self.feedback = QLabel()
        self.feedback.setWordWrap(True)
        content.addWidget(self.feedback)
        self.next_button = QPushButton("Sprawdź odpowiedź")
        self.next_button.clicked.connect(self.answer_or_next)
        self.next_button.hide()
        content.addWidget(self.next_button)
        self.flash_front = QLabel()
        self.flash_front.setWordWrap(True)
        self.flash_front.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flash_front.setMinimumHeight(130)
        content.addWidget(self.flash_front)
        self.flip_button = QPushButton("Pokaż odpowiedź")
        self.flip_button.clicked.connect(self.flip_card)
        self.flip_button.hide()
        content.addWidget(self.flip_button)
        self.flash_next = QPushButton("Następna fiszka")
        self.flash_next.clicked.connect(self.next_card)
        self.flash_next.hide()
        content.addWidget(self.flash_next)
        content.addStretch()
        self.stack.addWidget(page)
        self.refresh_notes()

    def choose_mode(self, mode):
        if self.busy:
            return
        self.mode = mode
        self.mode_title.setText("Quiz — pytania z AI" if mode == "quiz" else "Fiszki — powtórki z AI")
        self.clear_results()
        self.refresh_notes()
        self.stack.setCurrentIndex(1)

    def back_home(self):
        if not self.busy:
            self.stack.setCurrentIndex(0)

    def clear_results(self):
        self.question.clear()
        self.feedback.clear()
        self.flash_front.clear()
        for button in self.buttons:
            button.hide()
        self.next_button.hide()
        self.flip_button.hide()
        self.flash_next.hide()

    def refresh_notes(self):
        self.notes = self.repository.list_notes()
        previous = self.category.currentData()
        self.category.blockSignals(True)
        self.category.clear()
        self.category.addItem("Wszystkie kategorie", None)
        for category in sorted({note["category"] for note in self.notes}):
            self.category.addItem(category, category)
        index = self.category.findData(previous)
        self.category.setCurrentIndex(max(0, index))
        self.category.blockSignals(False)
        self.refresh_sources()

    def refresh_sources(self, *_):
        previous = self.source.currentData()
        category = self.category.currentData()
        filtered = [note for note in self.notes if category is None or note["category"] == category]
        self.source.clear()
        self.source.addItem("Wszystkie notatki w wybranej kategorii", "all")
        for note in filtered:
            self.source.addItem(note["title"], note["id"])
        index = self.source.findData(previous)
        if index >= 0:
            self.source.setCurrentIndex(index)

    def selected_material(self):
        category = self.category.currentData()
        filtered = [note for note in self.notes if category is None or note["category"] == category]
        source_id = self.source.currentData()
        if source_id != "all":
            filtered = [note for note in filtered if note["id"] == source_id]
        sections = []
        for note in filtered:
            parser = PlainText()
            parser.feed(self.storage.load(note["content_path"]))
            content = " ".join(parser.parts).strip()
            if content:
                sections.append(f"[{note['title']}]\n{content}")
        if not sections:
            raise ValueError("Brak niepustych notatek w wybranym zakresie.")
        material = "\n\n".join(sections)
        if len(material) > 12000:
            self.status.setText("Materiał jest długi; AI otrzyma pierwsze 12 000 znaków.")
        return (self.source.currentText() if source_id != "all" else (category or "Wszystkie kategorie")), material[:12000]

    def ai_config(self):
        if not self.settings:
            return {}
        light = self.settings.get("lightweight", False)
        return {
            "base_url": self.settings.get_ollama("base_url", "http://localhost:11434"),
            "model": self.settings.get_ollama("light_model", "qwen3:1.7b") if light else self.settings.get_ollama("model", "qwen3.5:4b"),
            "vision_model": self.settings.get_ollama("vision_model", "gemma3:4b")
        }

    def _ai_busy_changed(self, busy):
        self.generate.setEnabled(not busy)
        self.quiz_choice.setEnabled(not busy)
        self.flash_choice.setEnabled(not busy)

    def generate_material(self):
        if self.busy:
            return
        try:
            title, material = self.selected_material()
        except ValueError as error:
            QMessageBox.information(self, "Materiał", str(error))
            return
        if not ai_gate.claim():
            self.status.setText("AI jest zajęte innym zadaniem — poczekaj.")
            return
        self.clear_results()
        self.busy = True
        self.activity.emit("AI generuje " + ("quiz…" if self.mode == "quiz" else "fiszki…"))
        self.generate.setEnabled(False)
        self.quiz_choice.setEnabled(False)
        self.flash_choice.setEnabled(False)
        self.category.setEnabled(False)
        self.source.setEnabled(False)
        self.stack.setCurrentIndex(1)
        self.progress.show()
        self.status.setText("AI analizuje materiał i samodzielnie ustala liczbę " + ("pytań…" if self.mode == "quiz" else "fiszek…"))
        operation = "generate_quiz" if self.mode == "quiz" else "generate_flashcards"
        worker = AIWorker(operation, title, material, parent=self, **self.ai_config())
        self.worker = worker
        worker.succeeded.connect(lambda result, t=title: self.generation_success(t, result))
        worker.failed.connect(self.generation_failed)
        worker.finished.connect(self.generation_finished)
        worker.finished.connect(worker.deleteLater)
        try:
            worker.start()
        except Exception:
            ai_gate.release()
            raise

    def generation_finished(self):
        self.busy = False
        self.generate.setEnabled(not ai_gate._lock.locked())
        self.quiz_choice.setEnabled(not ai_gate._lock.locked())
        self.flash_choice.setEnabled(not ai_gate._lock.locked())
        self.category.setEnabled(True)
        self.source.setEnabled(True)
        self.progress.hide()
        self.worker = None

    def generation_failed(self, error):
        self.activity.emit("Błąd generowania: " + error)
        self.status.setText("Nie udało się wygenerować materiału: " + error)
        QMessageBox.warning(self, "AI", error)

    def generation_success(self, title, result):
        ProgressStore().record(generated=1)
        self.activity.emit("Gotowe: " + ("quiz" if self.mode == "quiz" else "fiszki") + f" — {len(result)} pozycji")
        if self.mode == "quiz":
            self.start_quiz(title, result)
        else:
            self.start_flashcards(title, result)

    def start_quiz(self, title, questions):
        self.mode = "quiz"
        self.stack.setCurrentIndex(1)
        self.clear_results()
        self.questions = questions
        self.quiz_started = monotonic()
        self.index = 0
        self.score = 0
        self.answered = False
        self.status.setText(f"Quiz: {title} · AI przygotowało {len(questions)} pytań")
        self.next_button.show()
        self.show_question()

    def show_question(self):
        if not self.questions:
            return
        self.answered = False
        item = self.questions[self.index]
        self.question.setText(f"{self.index + 1}/{len(self.questions)}. {item['question']}")
        self.group.setExclusive(False)
        for button, answer in zip(self.buttons, item["answers"]):
            button.setText(answer)
            button.setChecked(False)
            button.setEnabled(True)
            button.setStyleSheet("QRadioButton { padding: 10px; }")
            button.show()
        self.group.setExclusive(True)
        self.feedback.clear()
        self.next_button.setText("Sprawdź odpowiedź")

    def answer_or_next(self):
        if not self.questions:
            return
        if not self.answered:
            selected = self.group.checkedId()
            if selected < 0:
                self.feedback.setText("Wybierz odpowiedź.")
                return
            item = self.questions[self.index]
            correct = item["correct"]
            self.answered = True
            for i, button in enumerate(self.buttons):
                button.setEnabled(False)
                if i == correct:
                    button.setStyleSheet("QRadioButton { padding: 10px; color: #35b56a; }")
                elif i == selected:
                    button.setStyleSheet("QRadioButton { padding: 10px; color: #e05a5a; }")
            ProgressStore().record(correct=int(selected == correct), incorrect=int(selected != correct))
            if selected == correct:
                self.score += 1
                self.feedback.setText("Dobrze! +10 XP. " + item.get("explanation", ""))
            else:
                self.feedback.setText("Poprawna odpowiedź: " + item["answers"][correct] + ". " + item.get("explanation", ""))
            self.next_button.setText("Zakończ quiz" if self.index + 1 == len(self.questions) else "Następne pytanie")
            return
        self.index += 1
        if self.index >= len(self.questions):
            ProgressStore().record(seconds=monotonic()-self.quiz_started)
            self.activity.emit("Quiz ukończony — wynik " + f"{self.score}/{len(self.questions)}")
            self.status.setText(f"Ukończono! Wynik {self.score}/{len(self.questions)} · {self.score * 10} XP")
            self.question.setText("Quiz ukończony.")
            for button in self.buttons:
                button.hide()
            self.next_button.hide()
            return
        self.show_question()

    def start_flashcards(self, title, cards):
        self.mode = "cards"
        self.stack.setCurrentIndex(1)
        self.clear_results()
        self.cards = cards
        self.card_index = 0
        self.status.setText(f"Fiszki: {title} · AI przygotowało {len(cards)} fiszek")
        self.flip_button.show()
        self.flash_next.show()
        self.show_card()

    def show_card(self):
        if not self.cards:
            return
        self.flipped = False
        self.flash_front.setText(f"{self.card_index + 1}/{len(self.cards)}\n\n{self.cards[self.card_index]['front']}")
        self.flip_button.setText("Pokaż odpowiedź")

    def flip_card(self):
        if not self.cards:
            return
        self.flipped = not self.flipped
        key = "back" if self.flipped else "front"
        self.flash_front.setText(self.cards[self.card_index][key])
        self.flip_button.setText("Pokaż pytanie" if self.flipped else "Pokaż odpowiedź")

    def next_card(self):
        if self.cards:
            self.card_index = (self.card_index + 1) % len(self.cards)
            self.show_card()
