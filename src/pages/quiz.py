from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QRadioButton, QButtonGroup, QMessageBox
)


class QuizPage(QWidget):
    page_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("QuizPage")
        self.questions = []
        self.index = 0
        self.score = 0
        self.answered = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        self.title = QLabel("Questy wiedzy")
        self.title.setObjectName("PageTitle")
        self.subtitle = QLabel("Zamieniaj notatki w wyzwania i zdobywaj doświadczenie.")
        self.subtitle.setObjectName("PageSubtitle")
        self.progress = QLabel("")
        self.question = QLabel("Wygeneruj quiz z poziomu notatek, aby rozpocząć.")
        self.question.setWordWrap(True)
        self.question.setObjectName("SectionTitle")
        self.question.setMinimumHeight(90)

        self.answers_box = QVBoxLayout()
        self.group = QButtonGroup(self)
        self.buttons = []
        for i in range(4):
            button = QRadioButton()
            button.setMinimumHeight(44)
            button.setStyleSheet("QRadioButton { padding: 10px; }")
            self.group.addButton(button, i)
            self.answers_box.addWidget(button)
            self.buttons.append(button)

        self.feedback = QLabel("")
        self.feedback.setWordWrap(True)
        self.next_button = QPushButton("Sprawdź odpowiedź")
        self.next_button.setObjectName("PrimaryButton")
        self.next_button.clicked.connect(self.answer_or_next)
        self.back_button = QPushButton("Wróć do notatek")
        self.back_button.clicked.connect(lambda: self.page_requested.emit("notes"))

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(self.progress)
        layout.addWidget(self.question)
        layout.addLayout(self.answers_box)
        layout.addWidget(self.feedback)
        layout.addWidget(self.next_button)
        layout.addWidget(self.back_button)
        layout.addStretch()

    def start_quiz(self, title, questions):
        valid = []
        for item in questions:
            answers = item.get("answers")
            correct = item.get("correct")
            if (isinstance(item.get("question"), str)
                    and isinstance(answers, list) and len(answers) == 4
                    and isinstance(correct, int) and 0 <= correct < 4):
                valid.append(item)
        if not valid:
            QMessageBox.warning(self, "Quiz", "AI nie wygenerowało poprawnych pytań.")
            return
        self.questions = valid
        self.index = 0
        self.score = 0
        self.title.setText("Quest: " + title)
        self.show_question()

    def show_question(self):
        self.answered = False
        item = self.questions[self.index]
        self.progress.setText(
            f"Etap {self.index + 1}/{len(self.questions)} · XP: {self.score * 10}"
        )
        self.question.setText(item["question"])
        self.group.setExclusive(False)
        for button, answer in zip(self.buttons, item["answers"]):
            button.setText(answer)
            button.setChecked(False)
            button.setEnabled(True)
            button.show()
        self.group.setExclusive(True)
        self.feedback.setText("")
        self.next_button.setText("Sprawdź odpowiedź")

    def answer_or_next(self):
        if not self.answered:
            selected = self.group.checkedId()
            if selected < 0:
                self.feedback.setText("Wybierz odpowiedź.")
                return
            item = self.questions[self.index]
            correct = item["correct"]
            self.answered = True
            for index, button in enumerate(self.buttons):
                button.setEnabled(False)
                if index == correct:
                    button.setStyleSheet("QRadioButton { padding: 10px; color: #35b56a; }")
                elif index == selected:
                    button.setStyleSheet("QRadioButton { padding: 10px; color: #e05a5a; }")
            if selected == correct:
                self.score += 1
                self.feedback.setText("Dobrze! +10 XP\n" + item.get("explanation", ""))
            else:
                self.feedback.setText(
                    "Nie tym razem. Poprawna odpowiedź: "
                    + item["answers"][correct] + "\n" + item.get("explanation", "")
                )
            self.next_button.setText("Następne pytanie")
            return

        self.index += 1
        if self.index >= len(self.questions):
            total = len(self.questions)
            xp = self.score * 10
            QMessageBox.information(
                self, "Quest ukończony",
                f"Wynik: {self.score}/{total}\nZdobyte XP: {xp}"
            )
            self.question.setText("Quest ukończony!")
            self.progress.setText(f"XP: {xp}")
            self.next_button.setEnabled(False)
            return
        self.show_question()
