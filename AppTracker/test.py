import tkinter as tk      
import subprocess as process
from tkinter.messagebox import showerror
from tkinter import font  as tkfont
import requests, json, webbrowser
from Tracker import Tracker

tracker = Tracker()
class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.tracking = False
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.wm_title("VR Tracker")
        self.geometry('500x170')
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.bayid = ''
        self.setbayid()
        self.TRACKER_URI = '/Applications/Spotify.app/Contents/MacOS/Spotify'

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

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
    def sign_out(self):
        pass

    def setbayid(self):
        settings = self.getsettings()
        self.bayid = settings['bayid']
    
    def getsettings(self):
        with open("AppTracker/bin/tracker_config.json", "r") as tracker_config:
            return json.load(tracker_config)

    def writeconfig(self, data):
        with open("AppTracker/bin/tracker_config.json","w") as tracker_config:
            json.dump(data, tracker_config,indent=4)

    def getconfig(self, key):
        with open("AppTracker/bin/tracker_config.json", "r") as tracker_config:
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
                    #tracker.run()
                    process.call(["/Applications/Spotify.app/Contents/MacOS/Spotify"])
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

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='black')
        
        login_text = tk.StringVar()
        passd_text = tk.StringVar()
        login_label = tk.Label(self, text='Username or Email ->', font=('Helvetica', 14), pady=20, padx=20, background='black', fg='white')
        passw_label = tk.Label(self, text='Password ->', font=('bold', 16), pady=20, padx=20,fg='white', background='black')
        create_acc = tk.Label(self,text="Create Account!", fg="blue", cursor="hand2", background='black', bg='cyan')
        login_entry = tk.Entry(self, textvariable=login_text, font='Helvetica 15')
        passw_entry = tk.Entry(self, textvariable=passd_text, show='*',font='Helvetica 15')
        login_button = tk.Button(self, text='login', width=10, command=lambda: controller.login(login_entry.get(), passw_entry.get()))
        login_entry.grid(row=0, column=1)
        login_label.grid(row=0, column=0)
        passw_label.grid(row=1, column=0)
        passw_entry.grid(row=1, column=1)
        login_button.grid(row=2, column=1)        

class TrackerSwitch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Tracker is running...", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="PAUSE", command=lambda: tracker.pause())
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()