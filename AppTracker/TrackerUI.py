import tkinter as tk
import requests, webbrowser, json
from tkinter.messagebox import showerror
from Tracker import Tracker

class TrackerUI():
    def __init__(self, *args, **kwargs):
        self.app = tk.Tk()
        self.app.title("VR Tracker")
        self.app.geometry("400x200")
        self.app.configure(background='black')
        self.app.resizable(False, False)
        self.login_text = ''
        self.login_label = ''
        self.login_entry = ''
        self.passd_text = ''
        self.passw_label = ''
        self.passw_entry = ''
        self.login_button = ''
        self.create_acc = ''
        self.bayid = ''
        self.addLoginButton()
        self.addLoginTemplate()
        self.setbayid()
        self.centerApp()
        
    def centerApp(self):
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        size = tuple(int(_) for _ in self.app.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.app.geometry("+%d+%d" % (x, y))
    
    def addLoginTemplate(self):
        #Creating username lables and entry boxes
        self.login_text = tk.StringVar() # Text for login entry
        self.login_label = tk.Label(self.app, text='Username or Email', font=('Helvetica', 14), pady=20, padx=20, background='black', fg='cyan')
        self.login_label.grid(row=15, column=0) # Puting the label on the grid (gui)
        self.login_entry = tk.Entry(self.app, textvariable=self.login_text)
        self.login_entry.grid(row=15, column=1)

        # Password Labels and entry boxes
        self.passd_text = tk.StringVar() # Text for login entry
        self.passw_label = tk.Label(self.app, text='Password', font=('bold', 14), pady=20, padx=20,fg='cyan', background='black')
        self.passw_label.grid(row=16, column=0) # Puting the label on the grid (gui)
        self.passw_entry = tk.Entry(self.app, textvariable=self.passd_text, show='*')
        self.passw_entry.grid(row=16, column=1)
    
    def addLoginButton(self):
        # Buttons for logging in 
        
        self.login_button = tk.Button(self.app, text='login', width=12, command=lambda: self.login(self.login_entry.get(), self.passw_entry.get()), bg='cyan')
        self.login_button.grid(row=17, column=1)

        # link to account creation
        self.create_acc = tk.Label(self.app,text="Create Account!", fg="blue", cursor="hand2", background='black', bg='cyan')
        self.create_acc.bind("<Button-1>", lambda e: self.createaccount(""))
        self.create_acc.grid(row=19, column=1)
    
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

    def runTracker(self):
        Tracker.run()

    def handleLoginResponse(self, res, status, addingBay):
        try:
            if( status == 201 ):
                config = self.getsettings()
                config['tracked_games'] = res['tracked_games']
                print(addingBay)
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
    
    def createaccount(url):
        try:
            webbrowser.open_new(url)
        except webbrowser.Error() as err:
            print(err)

    def run(self):
        self.app.mainloop()