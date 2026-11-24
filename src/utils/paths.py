"""Resource paths for source and PyInstaller builds."""
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
else:
    RESOURCE_DIR = Path(__file__).resolve().parents[2]

ASSETS_DIR = RESOURCE_DIR / "assets"
