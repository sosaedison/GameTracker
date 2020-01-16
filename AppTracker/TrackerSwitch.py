import tkinter as tk
from Page import Page

class TrackerSwitch(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is TrackerSwitch")
        label.pack(side="top", fill="both", expand=True)
        but = tk.Button(self, text="Signout", height=5, width=50)
        but.pack(side='right')