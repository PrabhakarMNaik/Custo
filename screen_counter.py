import tkinter as tk
# from tkinter import *


def Start():

    def Count(Number):
        if Number == -1:
            win.withdraw()
            print("Start")  # what you want to do
            return False
        NumberLabel["text"] = Number
        win.after(1000, Count, Number-1)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    win = tk.Toplevel()
    # make it in the center.
    win.geometry("+%d+%d" % ((screen_width-win.winfo_width()) /
                 2, (screen_height-win.winfo_height())/2))
    win.overrideredirect(1)
    win.wm_attributes('-topmost', 1)  # top window
    # background transparent.
    win.wm_attributes('-transparentcolor', win['bg'])
    NumberLabel = tk.Label(win, font=("", 40, "bold"), fg='white')
    NumberLabel.pack()
    win.after(0, lambda: Count(10))
    win.mainloop()


root = tk.Tk()
root.title("our program")
start_cap = tk.Button(text='start recording', command=Start)
start_cap.pack()
root.mainloop()
