import tkinter as tk
from Page import Page
from tkinter.messagebox import showerror
import requests, webbrowser, json

class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is loginPage")
        label.pack(side="top", fill="both", expand=True)