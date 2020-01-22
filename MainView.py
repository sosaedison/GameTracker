import tkinter as tk
from tkinter import font as tkfont
from tkinter.messagebox import showerror
import requests, json, subprocess, psutil
from LoginPage import LoginPage
from TrackerSwitch import TrackerSwitch

class MainView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.tracking = False
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.switch_font = tkfont.Font(family='Helvetica', size=24, weight="bold", slant="italic")
        self.wm_title("VR Tracker")
        self.geometry('400x170')
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.bayid = ''
        self.setbayid()
        self.TRACKER_URI = "Tracker.exe"
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, TrackerSwitch):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if not self.trackerIsRunning():
            print("not running")
            if self.bayid != "":
                print("and logged in")
                self.startTracker()
                self.show_frame("TrackerSwitch")
            else:
                self.show_frame("LoginPage")
        else:
            print('running')
            self.show_frame("TrackerSwitch")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def startTracker(self):
        return subprocess.Popen([self.TRACKER_URI])

    def trackerIsRunning(self):
        try:
            for process in psutil.process_iter():
                if process.name() == "Tracker.exe":
                    return True
            return False
        except Exception as ex:
            print(ex)

    def stopTracker(self):
        try:
            while self.trackerIsRunning():
                for process in psutil.process_iter():
                    if process.name() == 'Tracker.exe':
                        process.terminate()
        except Exception as ex:
            print(ex)
            return False

    def setbayid(self):
        settings = self.getsettings()
        self.bayid = settings['bayid']
    
    def getsettings(self):
        with open(r"tracker_config.json", "r") as tracker_config:
            return json.load(tracker_config)

    def writeconfig(self, data):
        with open(r"tracker_config.json","w") as tracker_config:
            json.dump(data, tracker_config,indent=4)

    def getconfig(self, key):
        with open(r"tracker_config.json", "r") as tracker_config:
            settings = json.load(tracker_config)
            return settings[key]

    def handleLoginResponse(self, res, status, addingBay):
        try:
            if( status == 201 ):
                config = self.getsettings()
                config['tracked_games'] = res['tracked_games']
                if addingBay:
                    config['bayid'] = res['bayid']
                    config['userid'] = res['userid'] 
                self.writeconfig(config)
                return True
            else:
                return False # Tell user there was a server error on login
        except Exception as ex:
            print(ex) # Something went wrong with the config file...
            return False

    def login(self, eml, psswd):
        try:
            data = {
                "email" : eml,
                "password": psswd
            }
            if self.bayid != "":
                r = requests.post(self.getconfig("login_url"), json=data)
                response = json.loads(r.text) 
                if self.handleLoginResponse(response, r.status_code, False):
                    self.startTracker()
                    self.show_frame("TrackerSwitch")
                else:
                    showerror(title='Login Error', message='Wrong Email or Password')
            else:
                r = requests.post(self.getconfig("addbay_url"), json=data)
                response = json.loads(r.text)
                if self.handleLoginResponse(response, r.status_code, True):
                    print('pass add')
                    self.setbayid()
                else:
                    showerror(title='Login Error', message='Wrong Email or Password')
        except Exception as ex:
            print(ex)
            return False