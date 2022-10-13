import tkinter as tk


import psutil
import win32process
import win32gui
import time


root = tk.Tk()
root.title("our program")

program_dict = dict()

def active_window_process_name():
    # This produces a list of PIDs active window relates to
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    # pid[-1] is the most likely to survive last longer
    time.sleep(0.5)
    try:
        return psutil.Process(pid[-1]).name()
    except Exception:
        return ""


def get_screen_name():

    name = active_window_process_name()
    if name not in program_dict.keys():
        program_dict[name] = 0
    
    prog_dict = '\n'.join(key +":\t"+ str(value) for key, value in program_dict.items())
    NumberLabel["text"] = prog_dict
    win.after(1000, get_screen_name)
    pass

def Start_counting():
    # I want to print the active screen name on the
    #  active screen on the foreground
    global win 
    win = tk.Toplevel()
    global NumberLabel 
    NumberLabel = tk.Label(win, font=("", 10, "bold"), fg='white')
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
    win.mainloop()

start_cap = tk.Button(text='start recording', command=Start_counting)
start_cap.pack()
root.mainloop()