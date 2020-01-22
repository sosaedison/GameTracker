import tkinter as tk

class TrackerSwitch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='black')
        self.on = True
        self.label_text = tk.StringVar(self)
        self.label_text.set("Tracker is On...")
        label = tk.Label(self, textvariable=self.label_text, font=controller.switch_font, foreground='white', background='black')
        label.pack(side="top", fill="x", pady=10)
        self.pause_button_text = tk.StringVar(self)
        self.pause_button_text.set("PAUSE")
        button = tk.Button(self, textvariable=self.pause_button_text, command=lambda:self.pause() )
        button.pack()
    
    def changeRunningStatusText(self):
        if self.on:
            self.label_text.set("Tracker is On...")
        else:
            self.label_text.set("Tracker is Off")

    def changePauseButtonText(self):
        if self.on:
            self.pause_button_text.set("PAUSE")
        else:
            self.pause_button_text.set("START")
    
    def pause(self):
        if self.on:
            self.controller.stopTracker()
            self.on = False
            self.changePauseButtonText()
            self.changeRunningStatusText()
        else:
            self.controller.startTracker()
            self.on = True
            self.changePauseButtonText()
            self.changeRunningStatusText()
