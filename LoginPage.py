import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='black')
        
        login_text = tk.StringVar()
        passd_text = tk.StringVar()
        login_label = tk.Label(self, text='Email', font=('Helvetica', 14), pady=20, padx=20, background='black', fg='white')
        passw_label = tk.Label(self, text='Password', font=('Helvetica', 16), pady=20, padx=20,fg='white', background='black')
        create_acc = tk.Label(self,text="Create Account!", fg="blue", cursor="hand2", background='black', bg='cyan')
        login_entry = tk.Entry(self, textvariable=login_text, font='Helvetica 15')
        passw_entry = tk.Entry(self, textvariable=passd_text, show='*',font='Helvetica 15')
        login_button = tk.Button(self, text='login', width=10, command=lambda: controller.login(login_entry.get(), passw_entry.get()))
        login_entry.grid(row=0, column=1)
        login_label.grid(row=0, column=0)
        passw_label.grid(row=1, column=0)
        passw_entry.grid(row=1, column=1)
        login_button.grid(row=2, column=1)   