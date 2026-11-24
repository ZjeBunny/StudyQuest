
DARK_THEME = '''
* { font-size: 14px; font-family: "Segoe UI"; color: #e7e7e7; }
QMainWindow, QWidget { background: #111315; }
QLabel { background: transparent; }

QFrame#Sidebar {
    background: #151719;
    border-right: 1px solid #292d32;
}

QPushButton:hover { background: #292e35; }

QPushButton#NavButton {
    background: transparent;
    border: none;
    border-radius: 8px;
    min-height: 42px;
    max-height: 44px;
    text-align: left;
    padding: 12px 14px;
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
    min-width: 24px;
}

QLabel#NavIcon[selected="true"] {
    color: #A9C2EA;
}

QLabel#NavText {
    color: #B9C1CE;
    font-size: 13px;
    background: transparent;
}

QLabel#NavText[selected="true"] {
    color: #F0F3F8;
}

QLineEdit, QTextEdit, QComboBox {
    background: #181b1f;
    border: 1px solid #30353c;
    border-radius: 8px;
    padding: 8px;
}

QTextEdit { padding: 12px; }

QLabel#PageTitle { font-size: 28px; font-weight: 700; }
QLabel#PageSubtitle { color: #9299a3; font-size: 14px; }
QLabel#CardTitle { font-size: 16px; font-weight: 700; }

QFrame#Card {
    background: #181b1f;
    border: 1px solid #292e35;
    border-radius: 12px;
}

QListWidget {
    background: #181b1f;
    border: 1px solid #30353c;
    border-radius: 8px;
}

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

QLabel#SidebarSection {
    color: #737F91;
    font-size: 10px;
    font-weight: bold;
    padding-left: 14px;
}

QFrame#SidebarSeparator {
    background-color: #292F39;
    border: none;
}

QPushButton#SidebarToggle {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    color: #999999;
    min-height: 40px;
}

QPushButton#SidebarToggle:hover {
    background-color: rgba(128, 128, 128, 35);
    color: white;
}

QWidget#SettingsPage {
    background: transparent;
}

QScrollArea#SettingsScrollArea {
    background: transparent;
    border: none;
}

QWidget#SettingsContent {
    background: transparent;
}

QFrame#SettingsSection {
    background: #181b1f;
    border: 1px solid #292e35;
    border-radius: 12px;
}

QLabel#SettingsSectionTitle {
    font-size: 17px;
    font-weight: bold;
    color: #F0F1F5;
}

QLabel#SettingsSectionDescription {
    color: #9299a3;
    font-size: 12px;
}

QFrame#SettingsRow {
    background: transparent;
    border: none;
    border-bottom: 1px solid #292e35;
}

QLabel#SettingsRowTitle {
    color: #E7E7E7;
    font-size: 14px;
    font-weight: bold;
}

QLabel#SettingsRowDescription {
    color: #9299a3;
    font-size: 12px;
}

QLabel#SettingsVersion {
    color: #A8B8D8;
    font-weight: bold;
}

QComboBox, QSpinBox {
    min-width: 145px;
    min-height: 30px;
}

QFrame#NoteToolbar {
    background: transparent;
}

QSplitter::handle {
    background: #292e35;
    width: 1px;
}

QLineEdit#NoteTitleInput {
    font-size: 20px;
    font-weight: bold;
}

QWidget#NotesPage QPushButton {
    padding: 7px 12px;
}

QWidget#NotesPage QListWidget::item {
    padding: 9px;
}

/* Study chat: flexible history and compact composer */
QTextBrowser#StudyConversation {
    background: #181b1f;
    border: 1px solid #30353c;
    border-radius: 12px;
    padding: 10px;
}
QFrame#StudyComposer {
    background: #181b1f;
    border: 1px solid #30353c;
    border-radius: 12px;
}
QTextEdit#StudyQuestion {
    border: none;
    background: transparent;
    padding: 5px;
}
QLabel#StudyStatus { color: #94a3b8; font-size: 12px; }

/* Study chat: flexible history and compact composer */
QTextBrowser#StudyConversation {
    background: #181b1f;
    border: 1px solid #30353c;
    border-radius: 12px;
    padding: 10px;
}
QFrame#StudyComposer {
    background: #181b1f;
    border: 1px solid #30353c;
    border-radius: 12px;
}
QTextEdit#StudyQuestion {
    border: none;
    background: transparent;
    padding: 5px;
}
QLabel#StudyStatus { color: #94a3b8; font-size: 12px; }
'''


LIGHT_THEME = '''
* { font-size: 14px; font-family: "Segoe UI"; color: #202124; }
QMainWindow, QWidget { background: #f5f6f8; }
QLabel { background: transparent; }

QFrame#TitleBar {
    background: #F5F6F8;
    border-bottom: 1px solid #E0E3E8;
}

QFrame#Sidebar {
    background: #F0F2F5;
    border-right: 1px solid #DFE3E8;
}

QPushButton {
    background: #ffffff;
    border: 1px solid #d5d9de;
    border-radius: 8px;
}

QPushButton:hover {
    background: #eef0f3;
}

QPushButton#NavButton {
    text-align: left;
    border: none;
    background: transparent;
    padding: 12px 14px;
    min-height: 42px;
    max-height: 44px;
    border-radius: 8px;
}

QPushButton#NavButton:hover {
    background: #E5E9EF;
}

QPushButton#NavButton[selected="true"] {
    background: #DFE6F0;
    border-left: 3px solid #52698C;
}

QLabel#NavIcon {
    color: #778397;
    background: transparent;
    min-width: 24px;
}

QLabel#NavIcon[selected="true"] {
    color: #52698C;
}

QLabel#NavText {
    color: #596273;
    font-size: 13px;
    background: transparent;
}

QLabel#NavText[selected="true"] {
    color: #252832;
}

QLineEdit, QTextEdit, QComboBox {
    background: #ffffff;
    border: 1px solid #d5d9de;
    border-radius: 8px;
    padding: 8px;
}

QTextEdit { padding: 12px; }

QLabel#PageTitle {
    font-size: 28px;
    font-weight: 700;
}

QLabel#PageSubtitle {
    color: #68717c;
    font-size: 14px;
}

QLabel#CardTitle {
    font-size: 16px;
    font-weight: 700;
}

QFrame#Card {
    background: #ffffff;
    border: 1px solid #dfe3e8;
    border-radius: 12px;
}

QProgressBar {
    background: #e1e4e8;
    border: none;
    border-radius: 5px;
    height: 9px;
}

QProgressBar::chunk {
    background: #6b737d;
    border-radius: 5px;
}

QListWidget {
    background: #ffffff;
    border: 1px solid #d5d9de;
    border-radius: 8px;
}

QListWidget::item {
    padding: 10px;
}

QListWidget::item:selected {
    background: #dfe3e8;
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

QLabel#SidebarSection {
    color: #929AA7;
    font-size: 10px;
    font-weight: bold;
    padding-left: 14px;
}

QFrame#SidebarSeparator {
    background-color: #DFE3E8;
    border: none;
}

QPushButton#SidebarToggle {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    color: #999999;
    min-height: 40px;
}

QPushButton#SidebarToggle:hover {
    background-color: rgba(128, 128, 128, 35);
    color: #252832;
}

QWidget#SettingsPage {
    background: transparent;
}

QScrollArea#SettingsScrollArea {
    background: transparent;
    border: none;
}

QWidget#SettingsContent {
    background: transparent;
}

QFrame#SettingsSection {
    background: #FFFFFF;
    border: 1px solid #DFE3E8;
    border-radius: 12px;
}

QLabel#SettingsSectionTitle {
    font-size: 17px;
    font-weight: bold;
    color: #252832;
}

QLabel#SettingsSectionDescription {
    color: #858D99;
    font-size: 12px;
}

QFrame#SettingsRow {
    background: transparent;
    border: none;
    border-bottom: 1px solid #E8EBEF;
}

QLabel#SettingsRowTitle {
    color: #252832;
    font-size: 14px;
    font-weight: bold;
}

QLabel#SettingsRowDescription {
    color: #858D99;
    font-size: 12px;
}

QLabel#SettingsVersion {
    color: #52698C;
    font-weight: bold;
}

QComboBox, QSpinBox {
    min-width: 145px;
    min-height: 30px;
}

QFrame#NoteToolbar {
    background: transparent;
}

QSplitter::handle {
    background: #dfe3e8;
    width: 1px;
}

QLineEdit#NoteTitleInput {
    font-size: 20px;
    font-weight: bold;
}

QWidget#NotesPage QPushButton {
    padding: 7px 12px;
}

QWidget#NotesPage QListWidget::item {
    padding: 9px;
}
'''


THEMES = {"Light": (False,"#f7f9fc","#dce5f2","#c5d5eb","#ffffff","#345eaa"),
 "Dark": (True,"#121720","#202c3d","#30415a","#263244","#759be0"),
 "Green": (True,"#101c17","#20382c","#31513e","#253e30","#65c995"),
 "Purple": (True,"#191424","#30233f","#48345c","#392b4c","#c49af4"),
 "Kids": (False,"#fff8e9","#d9f2ed","#ffe0ac","#ffffff","#a33d88"),
 "Contrast": (True,"#000000","#202020","#353535","#101010","#ffdf45")}
CURRENT = {}
def palette(name, accent=""):
    from PySide6.QtGui import QColor
    dark, main, side, title, surface, default = THEMES.get(name, THEMES["Light"])
    a = QColor(accent) if accent else QColor(default)
    if not a.isValid(): a = QColor(default)
    def lum(c):
        channels = [c.redF(), c.greenF(), c.blueF()]
        return sum(w * (v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4) for w,v in zip((.2126,.7152,.0722), channels))
    def contrast(x,y):
        hi,lo = sorted((lum(x),lum(y)), reverse=True)
        return (hi+.05)/(lo+.05)
    if name == "Contrast":
        for _ in range(32):
            if all(contrast(a,QColor(bg)) >= 4.5 for bg in (main,side,title,surface)): break
            a = QColor.fromRgbF(*[v+(1-v)*.12 for v in (a.redF(),a.greenF(),a.blueF())])
    luminance = lum(a)
    a = a.name()
    return dict(dark=dark, main=main, side=side, title=title, surface=surface, accent=a, text="#ffffff" if dark else "#172033", button_text="#101010" if luminance > .179 else "#ffffff")
def scale_typography(css, font_size=14):
    import re
    ratio = max(10, min(24, int(font_size))) / 14
    return re.sub(r'(font-size:\s*)(\d+)px',
                  lambda m: f'{m[1]}{max(8, round(int(m[2])*ratio))}px', css)

def stylesheet(name, accent="", font_size=14):
    import re
    p = palette(name, accent); CURRENT.clear(); CURRENT.update(p); CURRENT["font_size"] = font_size
    base = DARK_THEME if p['dark'] else LIGHT_THEME
    base = re.sub(r'#(?:52698c|627fa9|405a80|829cc5|a9c2ea|8794a8|778397)',p['accent'],base,flags=re.I)
    css = base + f"""
QMainWindow, QWidget {{ background: {p['main']}; }}
QLabel {{ background: transparent; }}
QFrame#TitleBar {{ background: {p['title']}; }}
QFrame#Sidebar {{ background: {p['side']}; }}
QFrame#WelcomeCard, QFrame#FeatureCard, QFrame#SettingsSection, QFrame#StatCard, QTextBrowser, QTextEdit, QLineEdit, QComboBox, QTreeWidget {{ background: {p['surface']}; }}
QPushButton#PrimaryButton {{ background: {p['accent']}; color: {p['button_text']}; }}
QPushButton#PrimaryButton:hover {{ background: {p['accent']}; border: 2px solid {p['text']}; }}
QPushButton#NavButton[selected="true"] {{ background: {p['surface']}; border-left: 3px solid {p['accent']}; }}
QPushButton:disabled {{ color: #888888; background: {p['main']}; }}
QPushButton {{ background: {p['surface']}; border: 1px solid {p['accent']}; border-radius: 8px; padding: 8px; }}
QPushButton:hover {{ border: 2px solid {p['accent']}; background: {p['side']}; }}
QPushButton#QuizChoice {{ background: {p['surface']}; border: 2px solid {p['accent']}; border-radius: 14px; font-size: 19px; font-weight: bold; padding: 24px; }}
QPushButton#QuizChoice:hover {{ background: {p['side']}; }}
QPushButton#NavButton[compact="true"] {{ padding: 0; border: none; }}
QPushButton#NavButton[compact="true"][selected="true"] {{ border: 1px solid {p['accent']}; }}
QProgressBar {{ background: {p['side']}; border: none; min-height: 6px; max-height: 8px; border-radius: 3px; padding: 0; }}
QProgressBar::chunk {{ background: {p['accent']}; border-radius: 3px; }}
QPushButton#QuizAnswer {{ text-align: left; padding: 10px; }}
QPushButton#QuizAnswer:checked {{ border: 2px solid {p['accent']}; background: {p['side']}; }}
QPushButton#QuizAnswer[result="correct"] {{ color: {"#80efa8" if p['dark'] else "#176b36"}; border: 2px solid {"#80efa8" if p['dark'] else "#176b36"}; }}
QPushButton#QuizAnswer[result="wrong"] {{ color: {"#ff9292" if p['dark'] else "#a51d2d"}; border: 2px solid {"#ff9292" if p['dark'] else "#a51d2d"}; }}
"""

    from utils.paths import ASSETS_DIR
    check_path = (ASSETS_DIR / "icons/check_light.svg").as_posix() if p["button_text"] == "#ffffff" else (ASSETS_DIR / "icons/check_dark.svg").as_posix()
    control = max(18, round(font_size * 1.15))
    css += f"""
QLabel#NavText {{ font-weight: normal; }}
QLabel#NavText[selected="true"] {{ font-weight: bold; }}
QPushButton#NavButton {{ min-height: {max(42, font_size+20)}px; max-height: {max(44,font_size+24)}px; padding: 4px; }}
QPushButton#NavButton[compact="true"] {{ padding: 0; }}
QSpinBox, QComboBox {{ min-height: {max(30,font_size+12)}px; }}
QCheckBox::indicator {{ width: {control}px; height: {control}px; border: 2px solid {p['accent']}; border-radius: 4px; background: {p['surface']}; }}
QCheckBox::indicator:checked {{ background: {p['accent']}; image: url({check_path}); }}
"""
    return scale_typography(css, font_size)
