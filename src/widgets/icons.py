from pathlib import Path
from PySide6.QtCore import QByteArray, Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QLabel, QAbstractButton, QWidget
from themes.theme import CURRENT
ROOT = Path(__file__).resolve().parents[2] / 'assets/icons'
def pixmap(name, size=24):
    data=(ROOT / (name+'.svg')).read_text().replace('currentColor', CURRENT.get('accent','#52698c'))
    r=QSvgRenderer(QByteArray(data.encode())); p=QPixmap(size,size); p.fill(Qt.GlobalColor.transparent)
    painter=QPainter(p); r.render(painter); painter.end(); return p
def icon(name): return QIcon(pixmap(name))
def apply_icon(widget,name,size=24):
    widget.setProperty('svg_name',name); widget.setProperty('svg_size',size)
    size = round(size * min(1.3, max(0.9, CURRENT.get('font_size',14)/14)))
    if isinstance(widget,QLabel): widget.setText(''); widget.setPixmap(pixmap(name,size))
    elif isinstance(widget,QAbstractButton): widget.setIcon(QIcon(pixmap(name,size))); widget.setIconSize(QSize(size,size))
def refresh_icons(root):
    for w in root.findChildren(QWidget):
        if w.property('svg_name'): apply_icon(w,w.property('svg_name'),w.property('svg_size'))
