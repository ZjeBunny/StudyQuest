"""Consent-based local Ollama setup; downloads run in QProcess, not the GUI thread."""
import sys, shutil, json, os
from urllib.request import urlopen
from PySide6.QtCore import QObject, QProcess, QTimer, QProcessEnvironment
from PySide6.QtWidgets import QMessageBox, QProgressDialog
from ai.tools import ai_gate

class ModelSetup(QObject):
    def __init__(self, window):
        super().__init__(window); self.window=window; self.settings=window.settings_mng; self.process=None
    def ensure(self, models, callback=lambda ok: None):
        if self.process is not None:
            callback(False); return
        base=self.settings.get_ollama('base_url','http://localhost:11434').rstrip('/')
        try:
            with urlopen(base+'/api/tags',timeout=2) as r: names={x['name'] for x in json.load(r)['models']}
        except (OSError,ValueError,KeyError): names=None
        if names is not None and set(models)<=names: callback(True); return
        if not ai_gate.claim():
            QMessageBox.information(self.window,'AI','Poczekaj na zakończenie zadania AI.'); callback(False); return
        self.callback=callback; self.models=list(models); self.base=base
        if not shutil.which('ollama') and names is None:
            if QMessageBox.question(self.window,'Ollama','Nie znaleziono Ollama. Czy pobrać i zainstalować Ollama?') != QMessageBox.StandardButton.Yes:
                self.done(False); return
            if sys.platform=='win32' and shutil.which('winget'):
                self.run('winget',['install','--id','Ollama.Ollama','-e','--accept-package-agreements','--accept-source-agreements'],self.installed)
            elif sys.platform.startswith('linux'):
                # Use the official installer; authorization may be required in a terminal.
                QMessageBox.information(self.window,'Ollama','Instalator Linux może wymagać hasła administratora. Uruchom w terminalu: curl -fsSL https://ollama.com/install.sh | sh. Następnie ponów sprawdzanie.')
                self.done(False)
            else:
                QMessageBox.information(self.window,'Ollama','Zainstaluj Ollama z https://ollama.com/download i uruchom ponownie StudyQuest.'); self.done(False)
            return
        self.prepare(names)
    def installed(self,ok):
        if not ok: self.done(False); return
        QMessageBox.information(self.window,'Ollama','Instalacja zakończona. Uruchom ponownie StudyQuest, aby odświeżyć PATH i pobrać modele.'); self.done(False)
    def prepare(self,names):
        if names is None:
            from services.ollama_service import OllamaService
            self.server=OllamaService(self.base)
            if not self.server.start(): self.done(False); return
            try:
                with urlopen(self.base+'/api/tags',timeout=2) as r: names={x['name'] for x in json.load(r)['models']}
            except (OSError,ValueError,KeyError): self.done(False); return
        self.pending=[m for m in self.models if m not in names]
        if not self.pending: self.done(True); return
        if QMessageBox.question(self.window,'Modele AI','Pobrać brakujące modele?\n'+', '.join(self.pending)+'\nPobieranie może wymagać kilku GB miejsca.') != QMessageBox.StandardButton.Yes: self.done(False); return
        self.next_model(True)
    def next_model(self,ok):
        if not ok: self.done(False); return
        if not self.pending: self.done(True); return
        self.run('ollama',['pull',self.pending.pop(0)],self.next_model)
    def run(self,program,args,continuation):
        p=QProcess(self); self.process=p
        env=QProcessEnvironment.systemEnvironment(); env.insert('OLLAMA_HOST',self.base); p.setProcessEnvironment(env)
        dialog=QProgressDialog(' '.join(args),'Anuluj',0,0,self.window); dialog.setAutoClose(False); dialog.show()
        self.dialog=dialog
        def finish(ok):
            if self.process is not p: return
            self.process=None; dialog.close(); p.deleteLater(); continuation(ok)
        p.finished.connect(lambda code,status: finish(code==0 and status==QProcess.ExitStatus.NormalExit))
        p.errorOccurred.connect(lambda err: finish(False) if err==QProcess.ProcessError.FailedToStart else None)
        p.readyReadStandardError.connect(lambda: p.readAllStandardError())
        p.readyReadStandardOutput.connect(lambda: p.readAllStandardOutput())
        dialog.canceled.connect(p.kill); p.start(program,args)
    def done(self,ok):
        ai_gate.release(); self.window.refresh_ai_settings(); self.callback(ok)
