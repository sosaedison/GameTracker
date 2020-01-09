from tkinter import *
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
        self.addLoginButton()
        self.addLoginTemplate()
        
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

    def verifyBay(self, vfid):
        data = {"userid":vfid}
        r = requests.post(self.getconfig("verify_url"), json=data)
        response = json.loads(r.text)
        print(response)
    
    def handleLoginResponse(self, res, status):
        if( status != 500 ):
            print('Log in success')
            config = self.getsettings()
            config['tracked_games'] = res['games']
            print(config)
            self.verifyBay(vfid)
            #self.writeconfig(config)

    def login(self, eml, psswd):
        try:
            data = {
                "email" : eml,
                "password": psswd
            }
            r = requests.post(self.getconfig("login_url"), json=data)
            response = json.loads(r.text)
            return self.handleLoginResponse(response, r.status_code)
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

