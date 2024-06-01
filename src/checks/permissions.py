import psutil
import ctypes
from tkinter import messagebox


def check_isvalid_process() -> bool:
    check_variables = ["launcher.exe", "Wuthering Waves.exe"]
    PIDs = []
    process_running_check = False
    for process in psutil.process_iter():
        if process.name() in check_variables:
            PIDs.append(str(process.pid))
            process_running_check = True
    if process_running_check is True:
        PID_joined = "\n".join(PIDs)
        messagebox.showerror("Error",
                             f"Please close the game before proceeding.\n\nThe Unlocker checks if either \"launcher.exe\" or \"Wuthering Waves.exe is currently running.\"\n\nProcess IDs:\n{PID_joined}")
        return False
    else:
        return True


def admin_check() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
