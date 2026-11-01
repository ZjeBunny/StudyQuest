DARK_THEME = '''
* { font-family: "Segoe UI"; color: #e7e7e7; }
QMainWindow, QWidget { background: #111315; }
QLabel {background: transparent}
QFrame#Sidebar { background: #151719; border-right: 1px solid #292d32; }
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
QListWidget { background: #181b1f; border: 1px solid #30353c; border-radius: 8px; }
QListWidget::item { padding: 10px; }
QListWidget::item:selected { background: #2b3037; }

QFrame#TitleBar {
    background-color: #191B20;
    border-bottom: 1px solid #292C34;
}

QLabel#TitleLogo {
    color: #A8B8D8;
    font-size: 23px;
    font-weight: bold;
}

QLabel#TitleText {
    color: #F0F1F5;
    font-size: 19px;
    font-weight: bold;
}

QLabel#TitleSeparator {
    color: #555B68;
    font-size: 16px;
}

QLabel#CurrentPage {
    color: #B5BBC8;
    font-size: 13px;
}

QLabel#AIStatus {
    color: #E47777;
    font-size: 11px;
    padding: 0 8px;
}

QPushButton#TitleButton {
    background-color: transparent;
    color: #C5CAD4;
    border: none;
    border-radius: 6px;
    font-size: 21px;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
}

QPushButton#TitleButton:hover {
    background-color: #30343D;
}

QLineEdit#TitleSearch {
    background-color: #252932;
    color: #F0F1F5;
    border: 1px solid #3A404B;
    border-radius: 6px;
    padding: 5px 9px;
    selection-background-color: #52698C;
}

QFrame#TitleLine {
    background-color: #3A3D45;
}

QPushButton#WindowButton {
    background-color: #252932;
    color: #D8DCE5;
    border: 1px solid #343943;
    border-radius: 8px;
    min-width: 26px;
    max-width: 26px;
    min-height: 26px;
    max-height: 26px;
    font-size: 13px;
}

QPushButton#WindowButton:hover {
    background-color: #3A414D;
}

QPushButton#CloseButton {
    background-color: #252932;
    color: #D8DCE5;
    border: 1px solid #343943;
    border-radius: 8px;
    min-width: 26px;
    max-width: 26px;
    min-height: 26px;
    max-height: 26px;
    font-size: 17px;
}

QPushButton#CloseButton:hover {
    background-color: #bf001a;
    border-color: #8a001a;
    color: white;
}

QFrame#WelcomeCard {
    background: #202630;
    border: 1px solid #303947;
    border-radius: 16px;
}

QLabel#WelcomeTitle {
    color: #f0f1f5;
    font-size: 23px;
    font-weight: bold;
}

QLabel#WelcomeDescription {
    color: #aab3c2;
    font-size: 14px;
}

QLabel#SectionTitle {
    font-size: 19px;
    font-weight: bold;
}

QFrame#FeatureCard {
    background: #181b1f;
    border: 1px solid #30353c;
    border-radius: 12px;
}

QFrame#FeatureCard:hover {
    border: 1px solid #667b9e;
}

QLabel#FeatureIcon {
    font-size: 28px;
}

QPushButton#PrimaryButton {
    background: #52698c;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 11px 18px;
    font-weight: bold;
}

QPushButton#PrimaryButton:hover {
    background: #627fa9;
}

QPushButton#CardButton {
    background: transparent;
    color: #91acd6;
    border: none;
    padding: 5px 0;
}

QLabel#PageFooter {
    color: #737d8b;
    font-size: 12px;
}

QFrame#Sidebar {
    background-color: #15191F;
    border-right: 1px solid #292F39;
}

QLabel#SidebarSection {
    color: #737F91;
    font-size: 10px;
    font-weight: bold;
    padding-left: 14px;
}

QPushButton#NavButton {
    background: transparent;
    border: none;
    border-radius: 8px;
    min-height: 44px;
    max-height: 44px;
    text-align: left;
}

QPushButton#NavButton:hover {
    background-color: #222832;
}

QPushButton#NavButton[selected="true"] {
    background-color: #293547;
    border-left: 3px solid #829CC5;
}

QLabel#NavIcon {
    color: #8794A8;
    background: transparent;
    min-width: 22px;
}

QPushButton#NavButton[selected="true"] QLabel#NavIcon {
    color: #A9C2EA;
}

QLabel#NavText {
    color: #B9C1CE;
    font-size: 13px;
    background: transparent;
}

QPushButton#NavButton[selected="true"] QLabel#NavText {
    color: #F0F3F8;
    font-weight: bold;
}

QFrame#SidebarSeparator {
    background-color: #292F39;
    border: none;
}
'''

LIGHT_THEME = '''
* { font-family: "Segoe UI"; color: #202124; }
QMainWindow, QWidget { background: #f5f6f8; }
QLabel {background: transparent}
QFrame#TitleBar { background: #ffffff; border-bottom: 1px solid #dfe3e8; }
QFrame#Sidebar { background: #f0f2f5; border-right: 1px solid #dfe3e8; }
QPushButton { background: #ffffff; border: 1px solid #d5d9de; border-radius: 8px;}
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

QFrame#TitleBar {
    background-color: #F5F6F8;
    border-bottom: 1px solid #E0E3E8;
}

QLabel#TitleText {
    color: #252832;
    font-size: 19px;
    font-weight: bold;
}

QLabel#CurrentPage {
    color: #777E8B;
    font-size: 13px;
}

QPushButton#TitleButton {
    background-color: transparent;
    color: #252832;
    border: none;
    border-radius: 6px;
}

QPushButton#TitleButton:hover {
    background-color: #DDE1E8;
}

QPushButton#WindowButton,
QPushButton#CloseButton {
    background-color: #E9EBEF;
    color: #252832;
    border: 1px solid #E0E3E8;
    border-radius: 8px;
    min-width: 26px;
    max-width: 26px;
    min-height: 26px;
    max-height: 26px;
}

QPushButton#CloseButton:hover {
    background-color: #bf001a;
    border-color: #8a001a;
    color: white;
}

QFrame#WelcomeCard {
    background: #e9edf5;
    border: 1px solid #d8deea;
    border-radius: 16px;
}

QLabel#WelcomeTitle {
    color: #252832;
    font-size: 23px;
    font-weight: bold;
}

QLabel#WelcomeDescription {
    color: #68717c;
    font-size: 14px;
}

QLabel#SectionTitle {
    font-size: 19px;
    font-weight: bold;
}

QFrame#FeatureCard {
    background: #ffffff;
    border: 1px solid #dfe3e8;
    border-radius: 12px;
}

QFrame#FeatureCard:hover {
    border: 1px solid #8298ba;
}

QLabel#FeatureIcon {
    font-size: 28px;
}

QPushButton#PrimaryButton {
    background: #52698c;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 11px 18px;
    font-weight: bold;
}

QPushButton#PrimaryButton:hover {
    background: #405a80;
}

QPushButton#CardButton {
    background: transparent;
    color: #52698c;
    border: none;
    padding: 5px 0;
}

QLabel#PageFooter {
    color: #89919c;
    font-size: 12px;
}

QFrame#Sidebar {
    background-color: #F0F2F5;
    border-right: 1px solid #DFE3E8;
}

QLabel#SidebarSection {
    color: #929AA7;
    font-size: 10px;
    font-weight: bold;
    padding-left: 14px;
}

QPushButton#NavButton {
    background: transparent;
    border: none;
    border-radius: 8px;
    min-height: 44px;
    max-height: 44px;
}

QPushButton#NavButton:hover {
    background-color: #E5E9EF;
}

QPushButton#NavButton[selected="true"] {
    background-color: #DFE6F0;
    border-left: 3px solid #52698C;
}

QLabel#NavIcon {
    color: #778397;
    background: transparent;
    min-width: 22px;
}

QPushButton#NavButton[selected="true"] QLabel#NavIcon {
    color: #52698C;
}

QLabel#NavText {
    color: #596273;
    font-size: 13px;
    background: transparent;
}

QPushButton#NavButton[selected="true"] QLabel#NavText {
    color: #252832;
    font-weight: bold;
}

QFrame#SidebarSeparator {
    background-color: #DFE3E8;
    border: none;
}
'''
