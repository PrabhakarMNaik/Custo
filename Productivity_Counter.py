import tkinter as tk


import psutil
import win32process
import win32gui
import time
import cv2
import csv
import datetime
from datetime import date

FOLDER_PATH = "D:\Ekam\Daily_Log"
file_name = FOLDER_PATH + "\\" + str(date.today()) + ".csv"

def load_dict():
    try:
        with open(file_name, mode = "r") as f:
            reader = csv.reader(f)
            prog_dict = dict(reader)
            for key, value in prog_dict.items():
                prog_dict[key] = [float(value), time.time()]
            f.close()
            return prog_dict
    except FileNotFoundError:
        open(file_name, "x")
        return dict()

_font = cv2.FONT_HERSHEY_TRIPLEX
_fontscale = 1
_fontthk = 2
_fontcolor = (0, 0, 0)
_textcolorbg = (255, 255, 255)
margin = 3

root = tk.Tk()
root.title("Custodian")

program_dict = load_dict()


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


def get_screen_name():

    name = active_window_process_name()
    if name != "":
        if name not in program_dict.keys():
            program_dict[name] = [0, time.time()]
        else:
            program_dict[name][0] = program_dict[name][0] + \
                (time.time() - program_dict[name][1])
            program_dict[name][1] = time.time()

    prog_dict = '\n'.join(key + ":\t" + str(value[0])
                          for key, value in program_dict.items())
    NumberLabel["text"] = prog_dict
    win.after(1000, get_screen_name)
    pass


def Start_counting():
    # I want to print the active screen name on the
    #  active screen on the foreground
    global win
    win = tk.Toplevel()
    global NumberLabel
    NumberLabel = tk.Label(win, font=("", 10, "bold"), fg='white', bg="black")
    NumberLabel.pack()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    win.geometry("+%d+%d" % ((screen_width-win.winfo_width()) /
                 2, (screen_height-win.winfo_height())/2))
    win.overrideredirect(1)
    win.wm_attributes('-topmost', 1)  # top window
    # background transparent.
    win.wm_attributes('-transparentcolor', win['bg'])

    win.after(0, lambda: get_screen_name())
    # win.mainloop()

def Stop_counting():
    
    with open(file_name, mode= "w", encoding= "UTF8") as f:
        writer = csv.writer(f, lineterminator="\n")
        for key, value in program_dict.items():
            writer.writerow([key, value[0]])
        f.close()
    root.destroy()
    

start_cap = tk.Button(text='start recording', command=Start_counting)
start_cap.pack()

stop_cap = tk.Button(text='Stop recording', command=Stop_counting)
stop_cap.pack()

root.mainloop()
