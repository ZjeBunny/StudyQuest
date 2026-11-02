from PySide6.QtGui import QTextListFormat, QTextCharFormat, QTextBlockFormat, QFont
from PySide6.QtWidgets import QTextEdit, QColorDialog


class NoteEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(True)
        self.setPlaceholderText("Zacznij pisać swoją notatkę...")
        self.setTabChangesFocus(False)

    def insert_list(self):
        cursor = self.textCursor()
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.Style.ListDisc)
        cursor.createList(list_format)

    def set_heading(self, level):
        cursor = self.textCursor()
        cursor.beginEditBlock()

        block_format = QTextBlockFormat()
        char_format = QTextCharFormat()

        if level == 1:
            char_format.setFontPointSize(24)
            char_format.setFontWeight(QFont.Weight.Bold)

        elif level == 2:
            char_format.setFontPointSize(18)
            char_format.setFontWeight(QFont.Weight.Bold)

        else:
            char_format.setFontPointSize(12)
            char_format.setFontWeight(QFont.Weight.Normal)

        cursor.mergeBlockFormat(block_format)
        cursor.mergeCharFormat(char_format)

        cursor.endEditBlock()
        self.setTextCursor(cursor)

    
    def remove_text_formatting(self):
        cursor = self.textCursor()
        plain_format = QTextCharFormat()

        if cursor.hasSelection():
            cursor.setCharFormat(plain_format)
        else:
            cursor.mergeCharFormat(plain_format)

        self.setTextCursor(cursor)

    def choose_text_color(self):
        color = QColorDialog.getColor(self.textColor(), self)

        if color.isValid():
            text_format = QTextCharFormat()
            text_format.setForeground(color)
            self.mergeCurrentCharFormat(text_format)