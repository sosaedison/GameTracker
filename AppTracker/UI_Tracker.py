import tkinter as tk
from tkinter.messagebox import showerror
from Tracker import Tracker
from LoginPage import LoginPage
from MainView import MainView
from TrackerSwitch import TrackerSwitch
from Tracker import Tracker
import json
            
def main():
   

def stillLoggedIn():
    bayid = getconfig('bayid')
    if bayid != "":
        return True
    return False

def getconfig(key):
    with open("AppTracker/bin/tracker_config.json", "r") as tracker_config:
        settings = json.load(tracker_config)
        return settings[key]


if __name__ == "__main__":
    main()