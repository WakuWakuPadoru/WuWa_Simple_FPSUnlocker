import configparser
import sqlite3
import webbrowser
import glob
import os
import json
from tkinter import messagebox, Tk, StringVar, OptionMenu, Label, Checkbutton, Button
from tkinter.filedialog import askopenfilename
from pathlib import Path
from sys import exit

from checks.permissions import admin_check, check_isvalid_process

config = configparser.ConfigParser()
engine_config = configparser.ConfigParser(strict=False)


def choose_directory(action, root_window) -> None:
    if not check_isvalid_process():
        return
    possible_game_dirs = [
        "C:/Wuthering Waves/Wuthering Waves Game/",
        "C:/Program Files/Wuthering Waves/Wuthering Waves Game/",
        "D:/Wuthering Waves/Wuthering Waves Game/",
        "D:/Program Files/Wuthering Waves/Wuthering Waves Game/"
    ]
    game_dir = next((dir for dir in possible_game_dirs if os.path.exists(dir)), None)
    directory = askopenfilename(initialdir=game_dir,
                                title="Select where \"Wuthering Waves.exe\" is located.",
                                filetypes=[("exe files", "Wuthering Waves.exe")])
    userIsAdmin = admin_check()
    if "Program Files" in directory and not userIsAdmin:
        messagebox.showerror("Admin Rights",
                                "As your game is installed in Program Files, please run this program as an Administrator.")
        exit()
    path_dir_exe = Path(directory).parent.joinpath("Wuthering Waves.exe")
    path_dir_ext = Path(directory).parent.joinpath("Client", "Saved", "LocalStorage")
    path_dir_fs_cfg = Path(directory).parent.joinpath("Client", "Saved", "Config", "WindowsNoEditor",
                                                        "GameUserSettings.ini")
    path_dir_rt_cfg = Path(directory).parent.joinpath("Client", "Saved", "Config", "WindowsNoEditor",
                                                        "Engine.ini")
    path_dir_client_config_rt_json = Path(directory).parent.joinpath("Client", "Config", "RTX.json")
    path_dir_client_saved_sg_rt_json = Path(directory).parent.joinpath("Client", "Saved", "SaveGames",
                                                                        "RTX.json")
    if not path_dir_ext.is_dir() and not path_dir_exe.is_file():
        messagebox.showerror("Error",
                                "LocalStorage file not found. Please run the game at least once and try again!")
        return
    matching_files = sorted(glob.glob(glob.escape(str(path_dir_ext)) + "/LocalStorage*.db"))
    matching_files_length = len(matching_files)
    if matching_files_length != 1:
        match matching_files_length:
            case 0:
                messagebox.showerror("Error",
                                    "LocalStorage file not found. Please run the game at least once and try again!")
            case _:
                matching_files_oos = "\n".join(matching_files)
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
    messagebox.showinfo("Success", "File selected successfully!")
    # manage_fullscreen(path_dir_ext, path_dir_fs_cfg) # No longer possible due to Kuro games.
    match action:
        case "unlockFPS":
            fps_value(path_dir_ext, path_dir_fs_cfg)
        case "raytracing":
            raytracing_settings(path_dir_ext, path_dir_rt_cfg, path_dir_client_config_rt_json,
                            path_dir_client_saved_sg_rt_json, root_window)


# def manage_fullscreen(db_directory, path_dir_fs_cfg) -> None:
#     try:
#         config.read(path_dir_fs_cfg)
#         fs = config.get("/Script/Engine.GameUserSettings", "FullscreenMode")
#         last_fs = config.get("/Script/Engine.GameUserSettings", "LastConfirmedFullscreenMode")
#         pref_fs = config.get("/Script/Engine.GameUserSettings", "PreferredFullscreenMode")
#         fsm_list = [fs, last_fs, pref_fs]
#         fs_status = None
#
#         if min(fsm_list) == "0":
#             fs_status = "Enabled"
#         else:
#             fs_status = "Disabled"
#
#         current_x = config.get("/Script/Engine.GameUserSettings", "resolutionsizex")
#         current_y = config.get("/Script/Engine.GameUserSettings", "resolutionsizey")
#         fullscreen_mode_decision = messagebox.askyesno("True Fullscreen Mode",
#                                                        "Would you like to enable True Fullscreen Mode? (Optional)."
#                                                        "Click on \"Yes\" to enable or \"No\" to disable."
#                                                        "\n\nTrue Fullscreen Mode can lead to significantly better performance, increased smoothness, reduced stuttering, and reduced hitching"
#                                                        f"\n\nCurrent Status: {fs_status}\nCurrent Resolution: {current_x}x, {current_y}y")
#
#         if fullscreen_mode_decision is True:
#             resolution = simpledialog.askstring(title="Resolution",
#                                                 prompt="Choose your desired Resolution "
#                                                        "(E.g. 1280x720, 1920x1080, 2560x1440, and etc)\t\t\t",
#                                                 initialvalue=f"{current_x}x{current_y}")
#             if resolution is not None and resolution != "":
#                 x = resolution.split("x")[0]
#                 y = resolution.split("x")[1]
#                 while True:
#                     try:
#                         x = int(x)
#                         y = int(y)
#                         break
#                     except Exception as e:
#                         messagebox.showerror("Error",
#                                              "Please enter a valid Resolution (E.g. 1280x720, 1920x1080, 2560x1440, and etc)")
#
#                         resolution = simpledialog.askstring(title="Resolution",
#                                                             prompt="Please enter a valid Resolution (E.g. 1280x720, 1920x1080, 2560x1440, and etc)\t\t\t",
#                                                             initialvalue=f"{current_x}x{current_y}")
#
#                         if resolution is not None and resolution != "":
#                             x = resolution.split("x")[0]
#                             y = resolution.split("x")[1]
#                         else:
#                             x = x
#                             y = y
#
#                 db = sqlite3.connect(
#                     Path(db_directory).joinpath("LocalStorage.db"))
#                 cursor = db.cursor()
#                 cursor.execute("UPDATE LocalStorage SET Value = ? WHERE Key = 'PcResolutionWidth'",
#                                (str(x),))
#                 cursor.execute("UPDATE LocalStorage SET Value = ? WHERE Key = 'PcResolutionHeight'",
#                                (str(y),))
#                 db.commit()
#                 db.close()
#                 config.set("/Script/Engine.GameUserSettings", "lastuserconfirmedresolutionsizex", str(x))
#                 config.set("/Script/Engine.GameUserSettings", "lastuserconfirmedresolutionsizey", str(y))
#                 config.set("/Script/Engine.GameUserSettings", "resolutionsizex", str(x))
#                 config.set("/Script/Engine.GameUserSettings", "resolutionsizey", str(y))
#                 messagebox.OK = messagebox.showinfo("Success",
#                                                     "Resolution changed successfully!")
#             else:
#                 messagebox.showinfo("Info", "No Resolution selected, using current Resolution settings.")
#             config.set("/Script/Engine.GameUserSettings", "FullscreenMode", "0")
#             config.set("/Script/Engine.GameUserSettings", "LastConfirmedFullscreenMode", "0")
#             config.set("/Script/Engine.GameUserSettings", "PreferredFullscreenMode", "0")
#             with open(path_dir_fs_cfg, "w") as configfile:
#                 config.write(configfile)
#             messagebox.showinfo("Success", "True Fullscreen Mode enabled successfully!")
#         elif fullscreen_mode_decision is False:
#             config.set("/Script/Engine.GameUserSettings", "FullscreenMode", "1")
#             config.set("/Script/Engine.GameUserSettings", "LastConfirmedFullscreenMode", "1")
#             config.set("/Script/Engine.GameUserSettings", "PreferredFullscreenMode", "1")
#             with open(path_dir_fs_cfg, "w") as configfile:
#                 config.write(configfile)
#             messagebox.showinfo("Success", "True Fullscreen Mode disabled successfully!")
#
#     except TypeError as e:
#         if str(e) == "'NoneType' object is not subscriptable":
#             messagebox.showerror("Error",
#                                  "Your LocalStorage file has yet to be completed."
#                                  "Please run the game at least once and try again!")
#         else:
#             messagebox.showerror("Error",
#                                  f"An error occurred. Please raise an issue or contact me on the GitHub Page with the following message: \n\n{e}")
#             webbrowser.open("https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/issues")
#             # This shouldn't happen as this file should be generated by the game together with the LocalStorage file which was checked earlier.
#     except Exception as e:
#         messagebox.showerror("Error",
#                              f"An error occurred. "
#                              f"Please raise an issue or contact me on the GitHub Page with the following message: \n\n{e}")
#         webbrowser.open("https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/issues")


def fps_value(db_directory, path_dir_fs_cfg) -> None:
    try:
        messagebox.showinfo("INFORMATION", "Due to the 2.2 Update, the FPS Unlocker is now set to 120 FPS.")
        fps = 120
        db = sqlite3.connect(
            Path(db_directory).joinpath("LocalStorage.db"))
        cursor = db.cursor()
        # Create data structures
        menu_data_dict = {
            "___MetaType___": "___Map___",
            "Content": [
                [1, 100], [2, 100], [3, 100], [4, 100], [5, 0], [6, 0],
                [7, -0.4658685302734375], [10, 3], [11, 3], [20, 0], [21, 0],
                [22, 0], [23, 0], [24, 0], [25, 0], [26, 0], [27, 0], [28, 0],
                [29, 0], [30, 0], [31, 0], [32, 0], [33, 0], [34, 0], [35, 0],
                [36, 0], [37, 0], [38, 0], [39, 0], [40, 0], [41, 0], [42, 0],
                [43, 0], [44, 0], [45, 0], [46, 0], [47, 0], [48, 0], [49, 0],
                [50, 0], [51, 1], [52, 1], [53, 0], [54, 3], [55, 1], [56, 2],
                [57, 1], [58, 1], [59, 1], [61, 0], [62, 0], [63, 1], [64, 1],
                [65, 0], [66, 0], [67, 3], [68, 2], [69, 100], [70, 100], [79, 1],
                [81, 0], [82, 1], [83, 1], [84, 0], [85, 0], [87, 0], [88, 0],
                [89, 50], [90, 50], [91, 50], [92, 50], [93, 1], [99, 0], [100, 30],
                [101, 0], [102, 1], [103, 0], [104, 50], [105, 0], [106, 0.3],
                [107, 0], [112, 0], [113, 0], [114, 0], [115, 0], [116, 0],
                [117, 0], [118, 0], [119, 0], [120, 0], [121, 1], [122, 1],
                [123, 0], [130, 0], [131, 0], [132, 1], [135, 1], [133, 0]
            ]
        }

        play_menu_info_dict = {
            "1": 100, "2": 100, "3": 100, "4": 100, "5": 0, "6": 0,
            "7": -0.4658685302734375, "10": 3, "11": 3, "20": 0, "21": 0,
            "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0, "28": 0,
            "29": 0, "30": 0, "31": 0, "32": 0, "33": 0, "34": 0, "35": 0,
            "36": 0, "37": 0, "38": 0, "39": 0, "40": 0, "41": 0, "42": 0,
            "43": 0, "44": 0, "45": 0, "46": 0, "47": 0, "48": 0, "49": 0,
            "50": 0, "51": 1, "52": 1, "53": 0, "54": 3, "55": 1, "56": 2,
            "57": 1, "58": 1, "59": 1, "61": 0, "62": 0, "63": 1, "64": 1,
            "65": 0, "66": 0, "67": 3, "68": 2, "69": 100, "70": 100, "79": 1,
            "81": 0, "82": 1, "83": 1, "84": 0, "85": 0, "87": 0, "88": 0,
            "89": 50, "90": 50, "91": 50, "92": 50, "93": 1, "99": 0, "100": 30,
            "101": 0, "102": 1, "103": 0, "104": 50, "105": 0, "106": 0.3,
            "107": 0, "112": 0, "113": 0, "114": 0, "115": 0, "116": 0,
            "117": 0, "118": 0, "119": 0, "120": 0, "121": 1, "122": 1,
            "123": 0, "130": 0, "131": 0, "132": 1
        }

        # Remove the trigger if it exists
        cursor.execute("DROP TRIGGER IF EXISTS prevent_custom_frame_rate_update")

        # Create the trigger to prevent updates to the CustomFrameRate value
        trigger_sql = f"""
            CREATE TRIGGER prevent_custom_frame_rate_update
            AFTER UPDATE OF value ON LocalStorage
            WHEN NEW.key = 'CustomFrameRate'
            BEGIN
                UPDATE LocalStorage
                SET value = {fps}
                WHERE key = 'CustomFrameRate';
            END;
        """
        cursor.execute(trigger_sql)

        # Finally, update the FPS value
        cursor.execute(
            "UPDATE LocalStorage SET value = ? WHERE key = 'CustomFrameRate'",
            (fps,)
        )

        # Delete the old data if it exists for a clean state
        cursor.execute(
            "DELETE FROM LocalStorage WHERE key IN ('MenuData', 'PlayMenuInfo')"
        )

        # Prepare the new data for insertion
        insert_records = [
            ('MenuData', json.dumps(menu_data_dict)),
            ('PlayMenuInfo', json.dumps(play_menu_info_dict))
        ]

        # Batch insert the new data using parameterized queries
        cursor.executemany(
            "INSERT INTO LocalStorage (key, value) VALUES (?, ?)",
            insert_records
        )
        messagebox.OK = messagebox.showinfo("Success",
                                            "FPS Value changed successfully! You can now close this program and enjoy the game!")
        db.commit()
        db.close()
        config.read(path_dir_fs_cfg)
        config.set("/Script/Engine.GameUserSettings", "FrameRateLimit", str(fps))
        with open(path_dir_fs_cfg, "w") as configfile:
            config.write(configfile)

    except TypeError as e:
        if str(e) == "'NoneType' object is not subscriptable":
            messagebox.showerror("Error",
                                 "Your LocalStorage file is incomplete. Please run the game at least once and try again!")
        else:
            github_redirect_error(e)

    except sqlite3.OperationalError as e:
        if "attempt to write a readonly database" in str(e) and "Program Files" in str(db_directory):
            messagebox.showerror("Access Error",
                                 "As the game is installed in the Program Files directory, you may need to run this program with Admin Rights.")
            exit()

    except Exception as e:
        github_redirect_error(e)


def raytracing_settings(db_directory, path_dir_rt_cfg, path_dir_client_config_rt_json, path_dir_client_saved_sg_rt_json,
                        root_window) -> None:
    try:
        engine_config.read(path_dir_rt_cfg)
        if not engine_config.has_section("/Script/Engine.RendererRTXSettings"):
            engine_config.add_section("/Script/Engine.RendererRTXSettings")
        ask_RT = messagebox.askyesno("Enable Raytracing?",
                                     "Do you want to enable or disable Raytracing? \n\nYou will get lower FPS with Raytracing enabled. \n\nIt is recommended to have at least a RTX 2000 series or a RX 6000 series GPU for compatibility with DX12 Ultimate. \n\nClick Yes to access the Raytracing Options or No to disable Raytracing.")
        if ask_RT:
            root_window.withdraw()
            rt_window = Tk()
            rt_window.title("Raytracing Options")
            rt_window.geometry('400x200')
            preset_label = Label(rt_window, text="Select Raytracing Quality", font=("Bahnschrift", 12))
            preset_label.pack()
            rt_list = ["Low", "Medium", "High"]
            values_set = StringVar(rt_window)
            values_set.set("High")
            question_menu = OptionMenu(rt_window, values_set, *rt_list)
            question_menu.pack()
            reflections_value = StringVar(rt_window)
            reflections_value.set(1)
            rtgi_value = StringVar(rt_window)
            rtgi_value.set(1)
            reflections = Checkbutton(rt_window, text="Enable Raytracing Reflections", variable=reflections_value,
                                      onvalue=1, offvalue=0,
                                      font=("Bahnschrift", 12))
            reflections.pack(pady=(20, 0))
            rtgi = Checkbutton(rt_window, text="Enable Raytracing Global Illumination", variable=rtgi_value, onvalue=1,
                               offvalue=0,
                               font=("Bahnschrift", 12))
            rtgi.pack()
            submit_button = Button(rt_window, text='Submit',
                                   command=lambda: raytracing_apply(db_directory, path_dir_rt_cfg,
                                                                    path_dir_client_config_rt_json,
                                                                    path_dir_client_saved_sg_rt_json, root_window,
                                                                    values_set.get(), reflections_value.get(),
                                                                    rtgi_value.get(), rt_window),
                                   font=("Bahnschrift", 12))
            submit_button.pack(pady=(20, 0))
        else:
            db = sqlite3.connect(
                Path(db_directory).joinpath("LocalStorage.db"))
            cursor = db.cursor()
            db_settings = ["RayTracing", "RayTracedReflection", "RayTracedGI"]
            for key in db_settings:
                cursor.execute(
                    "INSERT INTO LocalStorage (Key, Value) VALUES (?, ?) "
                    "ON CONFLICT(Key) DO UPDATE SET Value = excluded.Value",
                    (key, 0),
                )
            db.commit()
            db.close()
            ray_tracing_settings = {
                "r.RayTracing": 0,
                "r.RayTracing.LimitDevice": 1,
                "r.RayTracing.EnableInGame": 0,
                "r.RayTracing.EnableOnDemand": 0,
                "r.RayTracing.EnableInEditor": 0,
            }
            for key, value in ray_tracing_settings.items():
                engine_config.set("/Script/Engine.RendererRTXSettings", key, str(value))
            ray_tracing_preset_keys = { # keys to remove after disabling rt
                "r.Lumen.ScreenProbeGather.DownsampleFactor",
                "r.Lumen.ScreenProbeGather.RadianceCache.ProbeResolution",
                "r.Lumen.ScreenProbeGather.RadianceCache.NumProbesToTraceBudget",
                "r.Lumen.ScreenProbeGather.TracingOctahedronResolution",
                "r.Lumen.ScreenProbeGather.ScreenTraces.HZBTraversal.FullResDepth",
                "r.Lumen.ScreenProbeGather.Temporal.DistanceThreshold",
                "r.Lumen.ScreenProbeGather.Temporal.MaxFramesAccumulated",
                "r.Lumen.Reflections.DownsampleFactor",
                "r.RayTracing.Shadows.MinScissorPercent",
                "r.Shadow.Denoiser.MinScissorPercent",
                "r.RayTracing.Shadows.MaxNumNoScissorCullLights",
                "r.Lumen.DiffuseIndirect.Allow",
                "r.Lumen.Reflections.Allow"
            }
            for key in ray_tracing_preset_keys:
                if engine_config.has_option("/Script/Engine.RendererRTXSettings", key):
                    engine_config.remove_option("/Script/Engine.RendererRTXSettings", key)
            with open(path_dir_rt_cfg, "w") as configfile:
                engine_config.write(configfile)
            rtDisable = {"bRayTracingEnable": 0}
            for path in [path_dir_client_config_rt_json, path_dir_client_saved_sg_rt_json]:
                with open(path, 'w') as rtxjson:
                    json.dump(rtDisable, rtxjson)
            messagebox.showinfo("Success", "Raytracing disabled successfully!")
            messagebox.showinfo("Info", "You can now close this program and enjoy the game!")
            root_window.destroy()
    except TypeError as e:
        if str(e) == "'NoneType' object is not subscriptable":
            messagebox.showerror("Error",
                                 "Your LocalStorage file is incomplete. Please run the game at least once and try again!")

    except sqlite3.OperationalError as e:
        if "attempt to write a readonly database" in str(e) and "Program Files" in str(db_directory):
            messagebox.showerror("Access Error",
                                 "As the game is installed in the Program Files directory, you may need to run this program with Admin Rights.")
            exit()

        else:
            github_redirect_error(e)
    except Exception as e:
        github_redirect_error(e)


def raytracing_apply(db_directory, path_dir_rt_cfg, path_dir_client_config_rt_json, path_dir_client_saved_sg_rt_json,
                     root_window, rt, rtref, rtgi, rt_window) -> None:
    engine_config.read(path_dir_rt_cfg)
    try:
        rt_value = None
        rt_preset = {
            'r.Lumen.DiffuseIndirect.Allow': int(rtgi),
            'r.Lumen.Reflections.Allow': int(rtref)
        }
        rt_preset_values = []
        rt_preset_keys = [ # all rt settings (order is important when filling in values!)
            "r.Lumen.ScreenProbeGather.DownsampleFactor",
            "r.Lumen.ScreenProbeGather.RadianceCache.ProbeResolution",
            "r.Lumen.ScreenProbeGather.RadianceCache.NumProbesToTraceBudget",
            "r.Lumen.ScreenProbeGather.TracingOctahedronResolution",
            "r.Lumen.ScreenProbeGather.ScreenTraces.HZBTraversal.FullResDepth",
            "r.Lumen.ScreenProbeGather.Temporal.DistanceThreshold",
            "r.Lumen.ScreenProbeGather.Temporal.MaxFramesAccumulated",
            "r.Lumen.Reflections.DownsampleFactor",
            "r.RayTracing.Shadows.MinScissorPercent",
            "r.Shadow.Denoiser.MinScissorPercent",
            "r.RayTracing.Shadows.MaxNumNoScissorCullLights"
        ]
        match rt:
            case "Low":
                rt_value = 1
                rt_preset_values = [64, 16, 180, 4, 0, 0.05, 30, 2, 0.6, 0.3, 3]  # low settings
            case "Medium":
                rt_value = 2
                rt_preset_values = [32, 32, 240, 6, 1, 0.03, 10, 1, 0.4, 0.2, 5]  # medium settings
            case "High":
                rt_value = 3
                rt_preset_values = [16, 32, 300, 8, 1, 0.005, 10, 1, 0, 0]  # high settings (the only preset not including MaxNumNoScissorCullLights)
                rt_preset_keys.remove("r.RayTracing.Shadows.MaxNumNoScissorCullLights")
        rt_preset.update({key: value for key, value in zip(rt_preset_keys, rt_preset_values)})
        db = sqlite3.connect(
            Path(db_directory).joinpath("LocalStorage.db"))
        cursor = db.cursor()
        db_settings = {
            "RayTracing": rt_value,
            "RayTracedReflection": int(rtref),
            "RayTracedGI": int(rtgi),
            "XessEnable": 0,
            "XessQuality": 0,
        }
        for key, value in db_settings.items():
            cursor.execute(
                "INSERT INTO LocalStorage (Key, Value) VALUES (?, ?) "
                "ON CONFLICT(Key) DO UPDATE SET Value = excluded.Value",
                (key, value),
            )
        db.commit()
        db.close()
        if engine_config.has_option("/Script/Engine.RendererRTXSettings", "r.RayTracing.Shadows.MaxNumNoScissorCullLights"): # kind of annoying to have this here but required if changing from medium or low to high
            engine_config.remove_option("/Script/Engine.RendererRTXSettings", "r.RayTracing.Shadows.MaxNumNoScissorCullLights")
        ray_tracing_settings = {
            "r.RayTracing": 1,
            "r.RayTracing.LimitDevice": 0,
            "r.RayTracing.EnableInGame": 1,
            "r.RayTracing.EnableOnDemand": 1,
            "r.RayTracing.EnableInEditor": 1,
        }
        ray_tracing_settings.update(rt_preset)
        for key, value in ray_tracing_settings.items():
            engine_config.set("/Script/Engine.RendererRTXSettings", key, str(value))
        with open(path_dir_rt_cfg, "w") as configfile:
            engine_config.write(configfile)
        rtEnable = {"bRayTracingEnable": 1}
        for path in [path_dir_client_config_rt_json, path_dir_client_saved_sg_rt_json]:
            with open(path, 'w') as rtxjson:
                json.dump(rtEnable, rtxjson)
        root_window.destroy()
        messagebox.showinfo("Success",
                            "Raytracing settings applied successfully!\n\nRestart the game once or twice for the settings to take effect.")
        messagebox.showinfo("Info", "You can now close this program and enjoy the game!")
        rt_window.destroy()
    except TypeError as e:
        if str(e) == "'NoneType' object is not subscriptable":
            messagebox.showerror("Error",
                                 "Your LocalStorage file is incomplete. Please run the game at least once and try again!")

    except sqlite3.OperationalError as e:
        if "attempt to write a readonly database" in str(e) and "Program Files" in str(db_directory):
            messagebox.showerror("Access Error",
                                 "As the game is installed in the Program Files directory, you may need to run this program with Admin Rights.")
            exit()

        else:
            github_redirect_error(e)
    except Exception as e:
        github_redirect_error(e)

def github_redirect_error(e):
    messagebox.showerror("Error",
                             f"An error occurred. Please raise an issue or contact me on the GitHub Page with the following message: \n\n{e}")
    webbrowser.open("https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/issues")