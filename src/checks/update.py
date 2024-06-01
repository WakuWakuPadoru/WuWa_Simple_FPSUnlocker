import requests
import webbrowser
from tkinter import messagebox

version = 0.67


def check_version() -> None:
    try:
        get_version = \
            float(
                requests.get(
                    "https://api.github.com/repos/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/releases/latest").json()[
                    "tag_name"][1:])
        if get_version > version:
            ask_update_dialog = messagebox.askyesno("Update Available",
                                                    f"An update is available!"
                                                    f"\nWould you like to view the latest release?"
                                                    f"\n\nCurrent Version: {version}\nLatest Version: {get_version}")
            if ask_update_dialog is True:
                webbrowser.open("https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/releases/latest")
            else:
                return

    except Exception as e:
        print(f"An error occurred while checking for updates: {e}")
        return
