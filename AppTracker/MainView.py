import tkinter as tk
from LoginPage import LoginPage
from TrackerSwitch import TrackerSwitch

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        loginpage = LoginPage(self)
        trackerswitch = TrackerSwitch(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        loginpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        trackerswitch.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        loginpage.show()