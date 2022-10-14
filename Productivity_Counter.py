import tkinter as tk

import psutil
import win32process
import win32gui
import time
import pyautogui

import csv

from datetime import date, timedelta


FOLDER_PATH = "D:\Ekam\Daily_Log"
file_name = FOLDER_PATH + "\\" + str(date.today()) + ".csv"


def load_dict():
    try:
        with open(file_name, mode="r") as f:
            reader = csv.reader(f)
            prog_dict = dict(reader)
            for key, value in prog_dict.items():
                prog_dict[key] = [float(value), time.time()]
            f.close()
            return prog_dict
    except FileNotFoundError:
        open(file_name, "x")
        return dict()


def active_window_process_name():
    # This produces a list of PIDs active window relates to
    process_ID = win32gui.GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(process_ID)
    # pid[-1] is the most likely to survive last longer
    time.sleep(0.5)
    try:
        return psutil.Process(pid[-1]).name()
    except Exception:
        return ""


root = tk.Tk()
root.geometry("300x70")
prev_name = active_window_process_name()
root.title("Custodian")


program_dict = load_dict()


def get_screen_time(prev_name, current_name):
    if current_name == prev_name:
        program_dict[current_name][0] = program_dict[current_name][0] + \
            (time.time() - program_dict[current_name][1])
    program_dict[current_name][1] = time.time()


def get_screen_name():
    global prev_name
    name = active_window_process_name().split(".")[0]
    if name != "":
        if name not in program_dict.keys():
            program_dict[name] = [0, time.time()]
        else:
            get_screen_time(prev_name, name)

    prog_dict = '\n'.join(key + ":" + str(timedelta(seconds=value[0])).split(".")[0]
                          for key, value in program_dict.items())
    NumberLabel["text"] = prog_dict
    prev_name = name
    display_screen()
    win.after(10, get_screen_name)


def display_screen():
    screen_width, screen_height = pyautogui.size()

    x, y = pyautogui.position()

    if x > screen_width - 50 and y > screen_height - 50:
        win_width, win_height = 0, 0
    else:
        win_width, win_height = screen_width, screen_height

    win.geometry("+%d+%d" % (win_width, win_height))


def Start_counting():
    # I want to print the active screen name on the
    #  active screen on the foreground

    global win
    win = tk.Toplevel()
    global NumberLabel
    NumberLabel = tk.Label(win, font=("", 10, "bold"),
                           fg='white', bg="black")
    NumberLabel.pack(side="left")

    win.overrideredirect(1)
    win.wm_attributes('-topmost', 1)  # top window
    # background transparent.
    win.wm_attributes('-transparentcolor', win['bg'])

    win.after(0, lambda: get_screen_name())


def Stop_counting():

    with open(file_name, mode="w", encoding="UTF8") as f:
        writer = csv.writer(f, lineterminator="\n")
        for key, value in program_dict.items():
            writer.writerow([key, value[0]])
        f.close()
    root.destroy()


start_cap = tk.Button(text='Start recording', command=Start_counting)
start_cap.pack(pady=5)

stop_cap = tk.Button(text='Stop recording', command=Stop_counting)
stop_cap.pack(pady=5)

root.mainloop()
