import psutil
import ctypes
from tkinter import messagebox


def check_isvalid_process() -> bool:
    if any(item in ["launcher.exe", "Wuthering Waves.exe"] for item in
           [p.name() for p in psutil.process_iter(attrs=['name'])]):
        messagebox.showerror("Error", "Please close the game before proceeding.")
        return False
    else:
        return True


def admin_check() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
