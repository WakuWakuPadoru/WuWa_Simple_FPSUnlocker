import glob
import json
import os
import sqlite3
import sys
import webbrowser
from pathlib import Path
import psutil
from tkinter import messagebox, Label, Button, Tk, CENTER, simpledialog
from tkinter.filedialog import askopenfilename
import requests

version = 0.5


def check_version():
    try:
        get_version = \
            float(
                requests.get(
                    "https://api.github.com/repos/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/releases/latest").json()[
                    "tag_name"][1:])
        if get_version > version:
            ask_update_dialog = messagebox.askyesno("Update Available",
                                                    f"An update is available!\nWould you like to view the latest release?\n\nCurrent Version: {version}\nLatest Version: {get_version}")
            if ask_update_dialog is True:
                webbrowser.open("https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/releases/latest")
            else:
                return
    except Exception as e:
        return


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def check_process_ok():
    if any(item in ["launcher.exe", "Wuthering Waves.exe"] for item in
           [p.name() for p in psutil.process_iter(attrs=['name'])]):
        messagebox.showerror("Error", "Please close the game before proceeding.")
        return False
    else:
        return True


def choose_directory():
    if check_process_ok() is True:
        directory = askopenfilename(initialdir="C:/Wuthering Waves/Wuthering Waves Game/",
                                    title="Select where \"Wuthering Waves.exe\" is located.",
                                    filetypes=[("exe files", "Wuthering Waves.exe")])
        if directory is not None and directory != "":
            path_dir_exe = Path(directory).parent.joinpath("Wuthering Waves.exe")
            path_dir_ext = Path(directory).parent.joinpath("Client", "Saved", "LocalStorage")
            if path_dir_ext.is_dir() and path_dir_exe.is_file():
                matching_files = sorted(glob.glob(str(path_dir_ext) + "/LocalStorage*.db"))
                matching_files_oos = "\n".join(matching_files)
                if len(matching_files) > 1:
                    messagebox.showerror("Error",
                                         "Multiple LocalStorage files found. This may cause compatibility issues with the FPS Unlocker."
                                         f"\n\n{matching_files_oos}"
                                         "\n\nThis is usually caused by game crashes or corruption with the original file. Please do the following before continuing:"
                                         "\n\n1) Click on OK to open the folder where the LocalStorage files are located. "
                                         "\n2) Make sure that the game and launcher isn't running and delete all files in the opened folder. (Your settings will be reset)."
                                         "\n3) Run the game at least once and close it to generate a new LocalStorage file."
                                         "\n4) Run this program again and it should work as intended.")

                    os.startfile(path_dir_ext)
                    return
                elif len(matching_files) == 0:
                    messagebox.showerror("Error",
                                         "LocalStorage file not found. Please run the game at least once and try again!")

                else:
                    messagebox.showinfo("Success", "File selected successfully!")
                    fps_value(path_dir_ext)
            else:
                messagebox.showerror("Error",
                                     "LocalStorage file not found. Please run the game at least once and try again!")
        else:
            return


def fps_value(directory):
    try:
        fps = simpledialog.askinteger(title="", prompt="Choose your desired FPS Value:\t\t\t", initialvalue=90,
                                      minvalue=60, maxvalue=240)
        if fps is not None:
            db = sqlite3.connect(
                Path(directory).joinpath("LocalStorage.db"))
            cursor = db.cursor()
            cursor.execute("SELECT * FROM LocalStorage WHERE Key = 'GameQualitySetting'")
            json_value = json.loads(cursor.fetchone()[1])
            json_value["KeyCustomFrameRate"] = fps
            cursor.execute("UPDATE LocalStorage SET Value = ? WHERE Key = 'GameQualitySetting'",
                           (json.dumps(json_value),))
            messagebox.OK = messagebox.showinfo("Success",
                                                "FPS Value changed successfully! You can now close this program and enjoy the game!")
            db.commit()
    except TypeError as e:
        if str(e) == "'NoneType' object is not subscriptable":
            messagebox.showerror("Error",
                                 "Your LocalStorage file is corrupted. Please delete it and run the game at least once to regenerate a new LocalStorage file and try again!"
                                 "The folder will be opened for you after you click OK.")
            os.startfile(directory)
        else:
            messagebox.showerror("Error",
                                 f"An error occurred. Please raise an issue or contact me on the GitHub Page with the following message: \n\n{e}")
            webbrowser.open("https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/issues")
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred. Please raise an issue or contact me on the GitHub Page with the following message: \n\n{e}")
        webbrowser.open("https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/issues")


root_window = Tk()
root_window.title(f"Wuthering Waves FPS Unlocker v{version}")
root_window.geometry("500x400")
root_window.iconbitmap(default=resource_path("./icon.ico"))
root_window.withdraw()
check_version()
root_window.deiconify()
label = Label(root_window, text=f"Welcome to the Wuthering Waves FPS Unlocker v{version}!"
                                "\n\n To get started, please click the \"Browse\" button below to locate the \"Wuthering Waves.exe\" file.\nMake sure that the game isn't running!"
                                "\n\n1) You may need to run this program again when you change graphical settings or when there's a new patch.\n2) This doesn't change the game files in any way, only your saved \"settings\".",
              font=("Bahnschrift", 14), wraplength=450, justify=CENTER)
label.pack()
button = Button(root_window, text="Browse", command=choose_directory, font=("Bahnschrift", 14))
button.pack(pady=(20, 10))
root_window.mainloop()
