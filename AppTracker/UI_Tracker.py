import tkinter as tk
from Tracker import Tracker
from LoginPage import LoginPage
from MainView import MainView
from TrackerSwitch import TrackerSwitch

if __name__ == "__main__":
    root = tk.Tk() # Use APP.py for tk???
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x200")
    root.resizable(False, False)
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2
    root.geometry("+%d+%d" % (x, y))
    root.mainloop()