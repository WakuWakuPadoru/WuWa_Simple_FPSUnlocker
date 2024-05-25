from tkinter import messagebox, Label, Button, Tk, CENTER, simpledialog
from tkinter.filedialog import askopenfilename
from pathlib import Path
import sqlite3
import json
import psutil


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
        if Path(directory).parent.joinpath("Wuthering Waves.exe").is_file():
            messagebox.showinfo("Success", "File selected successfully!")
            fps_value(directory)
        else:
            messagebox.showerror("Error", "File not found. Please try again.")
    else:
        return


def fps_value(directory):
    try:
        fps = simpledialog.askinteger(title="", prompt="Choose your desired FPS Value:\t\t\t", initialvalue=90,
                                      minvalue=60, maxvalue=240)
        if fps is not None:
            db = sqlite3.connect(
                Path(directory).parent.joinpath("Client", "Saved", "LocalStorage", "LocalStorage 2.db"))
            cursor = db.cursor()
            cursor.execute("SELECT * FROM LocalStorage WHERE Key = 'GameQualitySetting'")
            json_value = json.loads(cursor.fetchone()[1])
            json_value["KeyCustomFrameRate"] = fps
            cursor.execute("UPDATE LocalStorage SET Value = ? WHERE Key = 'GameQualitySetting'",
                           (json.dumps(json_value),))
            db.commit()
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred. Please raise an issue or contact me on the GitHub Page with the following message: \n\n{e}")
    messagebox.OK = messagebox.showinfo("Success", "FPS Value changed successfully!")

root_window = Tk()
root_window.title("Wuthering Waves FPS Unlocker")
root_window.geometry("500x400")
root_window.iconbitmap(default="icon.ico")
label = Label(root_window, text="Welcome to the Wuthering Waves FPS Unlocker!"
                                "\n\n To get started, please click the \"Browse\" button below to locate the \"Wuthering Waves.exe\" file.\nMake sure that the game isn't running!"
                                "\n\n1) You may need to run this program again when you change graphical settings or when there's a new patch.\n2) This doesn't change the game files in any way, only your saved \"settings\".",
              font=("Bahnschrift", 14), wraplength=450, justify=CENTER)
label.pack()
button = Button(root_window, text="Browse", command=choose_directory, font=("Bahnschrift", 14))
button.pack(pady=(20, 10))
root_window.mainloop()
