from tkinter import Label, Button, Tk, CENTER

from checks.update import *
from checks.permissions import *
from utils.util_helper import *
from config_modifiers.modifiers import *


def main() -> int:
    root_window = Tk()
    root_window.title(f"Wuthering Waves FPS Unlocker v{version}")
    root_window.geometry("650x550")
    root_window.iconbitmap(default=find_ico_path(r"icon.ico"))
    root_window.withdraw()
    if not admin_check():
        ask_admin = messagebox.askyesno("Admin Rights",
                                        "This program might require Admin Rights to function properly depending on where the game is installed (E.g. Program Files). "
                                        "\nWould you like to restart the program with Admin Rights?"
                                        "\n\nIn most cases, this is not required.")
        if ask_admin is True:
            # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None,
            #                                     1)  # IDE
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]),
                                                None, 1)  # EXE
            sys.exit()
        else:
            pass

    check_version()
    root_window.deiconify()
    label = Label(root_window, text=f"Welcome to Wuthering Waves FPS Unlocker Toolkit v.{version}!"
                                    "\n\nStep 1) Run the game at least once before using this tool or you might run into issues."
                                    "\nStep 2) Click on \"Browse\" to locate the \"Wuthering Waves.exe\" file. "
                                    "It should be located in a folder called \"Wuthering Waves Game\" in your game installation folder."
                                    "\n\nMake sure that the game isn't running!"
                                    "\n\n1) You may need to run this program again when you change graphical settings or when there's a new patch."
                                    "\n2) This doesn't change the game files in any way, only your saved \"settings\"."
                                    "\n\nDue to the 2.2 Update, you may need to restart the game twice after using the FPS Unlocker if it doesn't work the first time",
                  font=("Bahnschrift", 14), wraplength=590, justify=CENTER)

    label.pack()
    button = Button(root_window, text="Browse (FPS Unlock)", command=lambda: choose_directory("unlockFPS", root_window),
                    font=("Bahnschrift", 14))
    button.pack(pady=(20, 10))
    rt_button = Button(root_window, text="Raytracing Settings",
                       command=lambda: choose_directory("raytracing", root_window),
                       font=("Bahnschrift", 14))
    rt_button.pack(side="left", padx=(10, 10))
    root_window.mainloop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
