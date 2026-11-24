from widgets.icons import apply_icon, icon
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar,QGridLayout,QFrame,QScrollArea
from PySide6.QtCore import Qt
from services.progress import ProgressStore

class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        root=QVBoxLayout(self);root.setContentsMargins(32,28,32,28);root.setSpacing(15)
        title=QLabel("Moja przygoda");title.setObjectName("PageTitle");root.addWidget(title)
        sub=QLabel("Twoje osiągnięcia i postępy w nauce");sub.setObjectName("PageSubtitle");root.addWidget(sub)
        self.level=QLabel();self.level.setObjectName("SectionTitle");root.addWidget(self.level)
        self.bar=QProgressBar();self.bar.setFixedHeight(8);self.bar.setTextVisible(False);root.addWidget(self.bar);self.xp_label=QLabel();root.addWidget(self.xp_label)
        self.stats=QGridLayout();root.addLayout(self.stats)
        self.stat_labels=[]
        for i,name in enumerate(('🗒 Notatki','✓ Poprawne odpowiedzi','✕ Błędne odpowiedzi','⏱ Godziny nauki','⚡ Łącznie XP','✦ Wygenerowane zestawy')):
            box=QFrame();box.setObjectName('StatCard');v=QVBoxLayout(box)
            head=QLabel(name.split(" ",1)[-1]);v.addWidget(self.stat_icon(i));head.setObjectName('PageSubtitle');v.addWidget(head)
            value=QLabel('0');value.setObjectName('SectionTitle');v.addWidget(value)
            self.stat_labels.append(value);self.stats.addWidget(box,i//3,i%3)
        root.addWidget(QLabel('Odznaki za zdobyte poziomy'))
        self.badges=QLabel();self.badges.setWordWrap(True);root.addWidget(self.badges);root.addStretch()
        self.refresh()
    def stat_icon(self,i):
        label=QLabel();apply_icon(label,("notes","check","close","clock","bolt","cards")[i]);return label
    def refresh(self):
        d=ProgressStore().snapshot();self.level.setText(f"Poziom {d['level']}   •   {d['xp']} XP łącznie")
        self.bar.setMaximum(d['next_xp']);self.bar.setValue(d['progress']);self.xp_label.setText(f"{d['progress']} / {d['next_xp']} XP do następnego poziomu")
        values=[d['notes'],d['correct'],d['incorrect'],f"{d['seconds']/3600:.2f}",d['xp'],d['generated']]
        for label,value in zip(self.stat_labels,values):label.setText(str(value))
        self.badges.setText('   •   '.join(d['badges']) if d['badges'] else 'Zdobądź poziom 2, aby otrzymać pierwszą odznakę!')
