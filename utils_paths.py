# utils_paths.py
from pathlib import Path
import sys
import os

def app_dir() -> Path:
    """
    Retorna a pasta base da aplicação:
      - PyInstaller one-file: usa _MEIPASS
      - PyInstaller one-folder: usa a pasta do executável
      - Desenvolvimento: usa a pasta do projeto
    """
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass and os.path.isdir(meipass):
            return Path(meipass).resolve()
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


def data_path(*parts: str) -> Path:
    """Constrói um caminho relativo à pasta base detectada."""
    return app_dir().joinpath(*parts)