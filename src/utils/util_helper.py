import os
import sys


def find_ico_path(filename):
    try:
        base_path = sys._MEIPASS  # Required for PyInstaller
    except Exception:
        base_path = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(base_path, filename)
