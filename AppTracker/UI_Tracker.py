from tkinter import *
from tkinter.messagebox import showerror
import requests, webbrowser, json

class UITracker():

    def __init__(self):
        self.app = Tk()
        self.app.title("VR Tracker") # self.app title
        self.app.geometry("500x300") # self.app frame size
        self.app.configure(background='black')
        self.login_text = ''
        self.login_label = ''
        self.login_entry = ''
        self.passd_text = ''
        self.passw_label = ''
        self.passw_entry = ''
        self.login_button = ''
        self.create_acc = ''
        self.bayid = ''
        self.error_text =''
        self.addLoginButton()
        self.addLoginTemplate()
        self.setbayid()
        self.setErrorText()
        
    def addLoginTemplate(self):
        #Creating username lables and entry boxes
        self.login_text = StringVar() # Text for login entry
        self.login_label = Label(self.app, text='Username or Email', font=('Helvetica', 14), pady=20, padx=20, background='black', fg='cyan')
        self.login_label.grid(row=15, column=0, sticky=W) # Puting the label on the grid (gui)
        self.login_entry = Entry(self.app, textvariable=self.login_text)
        self.login_entry.grid(row=15, column=1)

        # Password Labels and entry boxes
        self.passd_text = StringVar() # Text for login entry
        self.passw_label = Label(self.app, text='Password', font=('bold', 14), pady=20, padx=20,fg='cyan', background='black')
        self.passw_label.grid(row=16, column=0, sticky=W) # Puting the label on the grid (gui)
        self.passw_entry = Entry(self.app, textvariable=self.passd_text, show='*')
        self.passw_entry.grid(row=16, column=1)

    def addLoginButton(self):
        # Buttons for logging in 
        self.login_button = Button(self.app, text='login', width=12, command=lambda: self.login(self.login_entry.get(), self.passw_entry.get()), bg='cyan')
        self.login_button.grid(row=17, column=1)

        # link to account creation
        self.create_acc = Label(self.app,text="Create Account!", fg="blue", cursor="hand2", background='black', bg='cyan')
        self.create_acc.bind("<Button-1>", lambda e: self.createaccount(""))
        self.create_acc.grid(row=19, column=1)
    
    def setbayid(self):
        settings = self.getsettings()
        self.bayid = settings['bayid']

    def setErrorText(self):
        self.error_text = Label(self.app, text='Error', fg='black', bg='black')
        self.error_text.grid(row=18, column=1)

    def showErrorText(self, error):
        self.error_text = Label(self.app, text="error", fg='red', bg='black')

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

    def handleLoginResponse(self, res, status):
        try:
            if( status != 500 ):
                print('Log in success')
                config = self.getsettings()
                config['tracked_games'] = res['games']
                config['bayid'] = res['bayid']
                self.writeconfig(config)
                print(config)
                return True
            print(res['error'])
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
            print("this")

            if self.bayid:
                r = requests.post(self.getconfig("login_url"), json=data)
                response = json.loads(r.text)
                if self.handleLoginResponse(response, r.status_code):
                    self.runTracker()
            else:
                r = requests.post(self.getconfig("addbay_url"), json=data)
                response = json.loads(r.text)
                if self.handleLoginResponse(response, r.status_code):
                    #self.runTracker()
                    pass
                else:
                    self.showErrorText("error")                    
                    # self.app.withdraw()
                    # showerror(title="Error",message="Could not add Bay")

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

def main():
    app = UITracker()
    app.run()
    
if __name__ == "__main__":
    main()

