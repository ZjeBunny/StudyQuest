from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLabel, QPushButton, QMenu
)


class NoteSidebar(QWidget):
    note_selected = Signal(str)
    new_note_requested = Signal()
    delete_category_requested = Signal(str)
    rename_category_requested = Signal(str)
    new_note_in_category_requested = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        heading = QLabel("Biblioteka notatek")
        heading.setObjectName("SectionTitle")
        layout.addWidget(heading)
        hint = QLabel("Rozwiń kategorię i wybierz notatkę. Kliknij kategorię prawym przyciskiem, aby ją usunąć.")
        hint.setWordWrap(True)
        hint.setObjectName("PageSubtitle")
        layout.addWidget(hint)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(24)
        self.tree.setAlternatingRowColors(True)
        self.tree.itemClicked.connect(self._clicked)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._context_menu)
        layout.addWidget(self.tree, 1)
        add = QPushButton("+ Nowa notatka")
        add.setObjectName("PrimaryButton")
        add.setMinimumHeight(42)
        add.clicked.connect(self.new_note_requested)
        layout.addWidget(add)

    def _clicked(self, item, column):
        note_id = item.data(0, Qt.ItemDataRole.UserRole)
        if note_id:
            self.note_selected.emit(note_id)
        else:
            item.setExpanded(not item.isExpanded())

    def _context_menu(self, pos):
        item = self.tree.itemAt(pos)
        if item is None or item.parent() is not None:
            return
        category = item.data(0, Qt.ItemDataRole.UserRole + 1)
        if not category:
            return
        menu = QMenu(self)
        create = menu.addAction("Nowa notatka w tej kategorii")
        rename = menu.addAction("Zmień nazwę kategorii…")
        menu.addSeparator()
        delete = menu.addAction("Usuń kategorię i jej notatki…")
        if category == "Bez kategorii":
            rename.setEnabled(False)
            delete.setEnabled(False)
        chosen = menu.exec(self.tree.viewport().mapToGlobal(pos))
        if chosen == create:
            self.new_note_in_category_requested.emit(category)
        elif chosen == rename:
            self.rename_category_requested.emit(category)
        elif chosen == delete:
            self.delete_category_requested.emit(category)

    def set_notes(self, notes, selected_id=None, categories=None):
        expanded = {
            self.tree.topLevelItem(i).data(0, Qt.ItemDataRole.UserRole + 1): self.tree.topLevelItem(i).isExpanded()
            for i in range(self.tree.topLevelItemCount())
        }
        self.tree.blockSignals(True)
        self.tree.clear()
        grouped = {category: [] for category in (categories or [])}
        for note in notes:
            grouped.setdefault(note['category'], []).append(note)
        for category in sorted(grouped, key=str.casefold):
            items = grouped[category]
            parent = QTreeWidgetItem([f"📁  {category}  ({len(items)})"])
            parent.setData(0, Qt.ItemDataRole.UserRole + 1, category)
            parent.setFlags(parent.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.tree.addTopLevelItem(parent)
            for note in items:
                child = QTreeWidgetItem(["📄  " + (note['title'] or 'Bez tytułu')])
                child.setData(0, Qt.ItemDataRole.UserRole, note['id'])
                child.setToolTip(0, note.get('tags', ''))
                parent.addChild(child)
            parent.setExpanded(expanded.get(category, True))
        self.tree.blockSignals(False)
