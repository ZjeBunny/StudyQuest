
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy
)


class StartPage(QWidget):
    page_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("StartPage")

        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(36, 30, 36, 30)
        main_layout.setSpacing(24)

        header = QVBoxLayout()
        header.setSpacing(8)

        title = QLabel("Witaj w StudyQuest!")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Twoje centrum nauki wspierane przez sztuczną inteligencję."
        )
        subtitle.setObjectName("PageSubtitle")

        header.addWidget(title)
        header.addWidget(subtitle)

        main_layout.addLayout(header)

        welcome_card = QFrame()
        welcome_card.setObjectName("WelcomeCard")

        welcome_layout = QVBoxLayout(welcome_card)
        welcome_layout.setContentsMargins(28, 26, 28, 26)
        welcome_layout.setSpacing(14)

        welcome_title = QLabel("Gotowy na kolejną dawkę wiedzy?")
        welcome_title.setObjectName("WelcomeTitle")

        welcome_description = QLabel(
            "Rozwiązuj zadania, poznawaj nowe zagadnienia "
            "i korzystaj z pomocy lokalnego asystenta AI."
        )
        welcome_description.setObjectName("WelcomeDescription")
        welcome_description.setWordWrap(True)

        start_button = QPushButton("Rozpocznij naukę")
        start_button.setObjectName("PrimaryButton")
        start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        start_button.clicked.connect(
            lambda: self.page_requested.emit("study")
        )

        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_description)
        welcome_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addWidget(welcome_card)

        section_title = QLabel("Szybki dostęp")
        section_title.setObjectName("SectionTitle")

        main_layout.addWidget(section_title)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        cards = [
            ("📚", "Nauka", "Ucz się z pomocą AI.", "study"),
            ("📝", "Notatki", "Twórz i organizuj notatki.", "notes"),
            ("🧠", "Quizy", "Sprawdź swoją wiedzę.", "quiz")
        ]

        for icon, title, description, page in cards:
            card = self.create_card(icon, title, description, page)
            cards_layout.addWidget(card)

        main_layout.addLayout(cards_layout)

        main_layout.addStretch()

        footer = QLabel("StudyQuest • Ucz się mądrzej, nie ciężej.")
        footer.setObjectName("PageFooter")

        main_layout.addWidget(footer)

    def create_card(self, icon, title, description, page):
        card = QFrame()
        card.setObjectName("FeatureCard")
        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setObjectName("FeatureIcon")

        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")

        description_label = QLabel(description)
        description_label.setObjectName("PageSubtitle")
        description_label.setWordWrap(True)

        button = QPushButton("Otwórz →")
        button.setObjectName("CardButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(
            lambda: self.page_requested.emit(page)
        )

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)

        return card
