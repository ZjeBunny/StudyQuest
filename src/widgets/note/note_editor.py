from PySide6.QtCore import Qt, QMarginsF
from PySide6.QtGui import (
    QTextBlockFormat, QTextCharFormat, QTextCursor, QTextDocument,
    QTextImageFormat, QTextListFormat, QFont
)
from PySide6.QtWidgets import QTextEdit, QColorDialog, QFileDialog, QMessageBox


class NoteEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(True)
        self.setPlaceholderText("Zacznij pisać swoją notatkę...")
        self.setTabChangesFocus(False)
        self.setUndoRedoEnabled(True)
        self.document().setDefaultFont(QFont("Segoe UI", 11))

    def _apply_block(self, style, size, weight=QFont.Weight.Normal):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        block = QTextBlockFormat()
        block.setHeadingLevel(style)
        char = QTextCharFormat()
        char.setFontPointSize(size)
        char.setFontWeight(weight)
        cursor.mergeBlockFormat(block)
        cursor.mergeCharFormat(char)
        self.setTextCursor(cursor)
        cursor.endEditBlock()
        self.setFocus()

    def set_heading(self, level):
        if level == 1:
            self._apply_block(1, 22, QFont.Weight.Bold)
        elif level == 2:
            self._apply_block(2, 17, QFont.Weight.Bold)
        else:
            self._apply_block(0, 11, QFont.Weight.Normal)

    def set_normal_text(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        block = QTextBlockFormat()
        block.setHeadingLevel(0)
        block.setObjectIndex(-1)
        char = QTextCharFormat()
        char.setFontPointSize(11)
        char.setFontWeight(QFont.Weight.Normal)
        char.setFontItalic(False)
        char.setFontUnderline(False)
        char.setForeground(self.palette().text().color())
        cursor.mergeBlockFormat(block)
        cursor.mergeCharFormat(char)
        self.setTextCursor(cursor)
        cursor.endEditBlock()
        self.setFocus()

    def insert_list(self, ordered=False):
        cursor = self.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(
            QTextListFormat.Style.ListDecimal if ordered
            else QTextListFormat.Style.ListDisc
        )
        cursor.createList(fmt)
        self.setTextCursor(cursor)
        self.setFocus()

    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(
            QFont.Weight.Normal if self.fontWeight() >= QFont.Weight.Bold
            else QFont.Weight.Bold
        )
        self.mergeCurrentCharFormat(fmt)
        self.setFocus()

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self.fontItalic())
        self.mergeCurrentCharFormat(fmt)
        self.setFocus()

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not self.fontUnderline())
        self.mergeCurrentCharFormat(fmt)
        self.setFocus()

    def choose_text_color(self):
        color = QColorDialog.getColor(self.textColor(), self, "Kolor tekstu")
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.mergeCurrentCharFormat(fmt)
            self.setFocus()

    def insert_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Wstaw obraz", "",
            "Obrazy (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if not path:
            return
        cursor = self.textCursor()
        image = QTextImageFormat()
        image.setName(path)
        image.setWidth(480)
        cursor.insertImage(image)
        self.setTextCursor(cursor)
        self.setFocus()

    def insert_html(self, html):
        self.textCursor().insertHtml(html)
        self.setFocus()

    def export_pdf(self, parent=None):
        path, _ = QFileDialog.getSaveFileName(
            parent or self, "Eksportuj notatkę do PDF", "notatka.pdf",
            "Pliki PDF (*.pdf)"
        )
        if not path:
            return False
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        from PySide6.QtGui import QPageLayout, QPageSize, QPdfWriter
        writer = QPdfWriter(path)
        writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        writer.setPageMargins(QMarginsF(15, 15, 15, 15), QPageLayout.Unit.Millimeter)
        self.document().print_(writer)
        return True
