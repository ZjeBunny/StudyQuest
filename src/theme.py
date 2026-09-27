DARK_THEME = '''
* { font-family: "Segoe UI"; color: #e7e7e7; }
QMainWindow, QWidget { background: #111315; }
QLabel {background: transparent}
QFrame#TitleBar { background: #17191c; border-bottom: 1px solid #292d32; }
QFrame#Sidebar { background: #151719; border-right: 1px solid #292d32; }
QPushButton { background: #20242a; border: 1px solid #2c3239; border-radius: 8px; }
QPushButton#minimizeapp:hover { background: yellow;}
QPushButton#maximizeapp:hover { background: blue;}
QPushButton#exitapp:hover { background: red;}
QPushButton:hover { background: #292e35; }
QPushButton#NavButton { text-align: left; border: none; background: transparent; padding: 12px 14px; }
QPushButton#NavButton:hover { background: #22262b; }
QPushButton#NavButton[selected="true"] { background: #2b3037; }
QLineEdit, QTextEdit, QComboBox { background: #181b1f; border: 1px solid #30353c; border-radius: 8px; padding: 8px; }
QTextEdit { padding: 12px; }
QLabel#PageTitle { font-size: 28px; font-weight: 700; }
QLabel#PageSubtitle { color: #9299a3; font-size: 14px; }
QLabel#CardTitle { font-size: 16px; font-weight: 700; }
QFrame#Card { background: #181b1f; border: 1px solid #292e35; border-radius: 12px; }
QProgressBar { background: #24282e; border: none; border-radius: 5px; height: 9px; }
QProgressBar::chunk { background: #bfc6ce; border-radius: 5px; }
QListWidget { background: #181b1f; border: 1px solid #30353c; border-radius: 8px; }
QListWidget::item { padding: 10px; }
QListWidget::item:selected { background: #2b3037; }
'''

LIGHT_THEME = '''
* { font-family: "Segoe UI"; color: #202124; }
QMainWindow, QWidget { background: #f5f6f8; }
QLabel {background: transparent}
QFrame#TitleBar { background: #ffffff; border-bottom: 1px solid #dfe3e8; }
QFrame#Sidebar { background: #f0f2f5; border-right: 1px solid #dfe3e8; }
QPushButton { background: #ffffff; border: 1px solid #d5d9de; border-radius: 8px;}
QPushButton#minimizeapp:hover { background: yellow;}
QPushButton#maximizeapp:hover { background: blue;}
QPushButton#exitapp:hover { background: red;}
QPushButton:hover { background: #eef0f3; }
QPushButton#NavButton { text-align: left; border: none; background: transparent; padding: 12px 14px; }
QPushButton#NavButton:hover { background: #e7e9ed; }
QPushButton#NavButton[selected="true"] { background: #dfe3e8; }
QLineEdit, QTextEdit, QComboBox { background: #ffffff; border: 1px solid #d5d9de; border-radius: 8px; padding: 8px; }
QTextEdit { padding: 12px; }
QLabel#PageTitle { font-size: 28px; font-weight: 700; }
QLabel#PageSubtitle { color: #68717c; font-size: 14px; }
QLabel#CardTitle { font-size: 16px; font-weight: 700; }
QFrame#Card { background: #ffffff; border: 1px solid #dfe3e8; border-radius: 12px; }
QProgressBar { background: #e1e4e8; border: none; border-radius: 5px; height: 9px; }
QProgressBar::chunk { background: #6b737d; border-radius: 5px; }
QListWidget { background: #ffffff; border: 1px solid #d5d9de; border-radius: 8px; }
QListWidget::item { padding: 10px; }
QListWidget::item:selected { background: #dfe3e8; }
'''
