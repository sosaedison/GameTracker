import tkinter as tk
from Page import Page
from tkinter.messagebox import showerror
from Tracker import Tracker
import requests, webbrowser, json

class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        login_text = tk.StringVar()
        passd_text = tk.StringVar()
        login_button = tk.Button(self, text='login', width=10, command=lambda: self.login(login_entry.get(), passw_entry.get()), bg='cyan')
        login_label = tk.Label(self, text='Username or Email ->', font=('Helvetica', 14), pady=20, padx=20, background='black', fg='cyan')
        passw_label = tk.Label(self, text='Password ->', font=('bold', 16), pady=20, padx=20,fg='cyan', background='black')
        create_acc = tk.Label(self,text="Create Account!", fg="blue", cursor="hand2", background='black', bg='cyan')
        login_entry = tk.Entry(self, textvariable=login_text, font='Helvetica 20')
        passw_entry = tk.Entry(self, textvariable=passd_text, show='*',font='Helvetica 20')
        login_entry.grid(row=0, column=1)
        login_label.grid(row=0, column=0)
        passw_label.grid(row=1, column=0)
        passw_entry.grid(row=1, column=1)
        login_button.grid(row=2, column=1)
        #create_acc.grid(row=3, column=1)
        self.bayid = ''
        self.setbayid()

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
                    #self.runTracker()
                    print('pass login')
                    showerror(title="LOGGED IN", message="Login Successful! You can close these windows.")
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

    def createaccount(url):
        try:
            webbrowser.open_new(url)
        except webbrowser.Error() as err:
            print(err)

    def runTracker(self):
        Tracker.run()