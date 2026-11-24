@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    python -m venv .venv || exit /b 1
)
.venv\Scripts\python.exe -m pip install -r requirements.txt pyinstaller || exit /b 1
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --onedir --name StudyQuest --paths src --add-data "assets;assets" src/main.py || exit /b 1
echo Build complete: dist\StudyQuest\StudyQuest.exe
