import tkinter as tk       
from tkinter import font  as tkfont

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.tracking = False
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.wm_title("VR Tracker")
        self.geometry('500x170')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
    def sign_out(self):
        pass

    def run_tracker(self):
        pass

    def pause_tracker(self):
        pass


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='black')
        
        login_text = tk.StringVar()
        passd_text = tk.StringVar()
        login_label = tk.Label(self, text='Username or Email ->', font=('Helvetica', 14), pady=20, padx=20, background='black', fg='cyan')
        passw_label = tk.Label(self, text='Password ->', font=('bold', 16), pady=20, padx=20,fg='cyan', background='black')
        create_acc = tk.Label(self,text="Create Account!", fg="blue", cursor="hand2", background='black', bg='cyan')
        login_entry = tk.Entry(self, textvariable=login_text, font='Helvetica 20')
        passw_entry = tk.Entry(self, textvariable=passd_text, show='*',font='Helvetica 20')
        login_button = tk.Button(self, text='login', width=10)
        login_entry.grid(row=0, column=1)
        login_label.grid(row=0, column=0)
        passw_label.grid(row=1, column=0)
        passw_entry.grid(row=1, column=1)
        login_button.grid(row=2, column=1)

        # button1 = tk.Button(self, text="Go to Page One",
        #                     command=lambda: controller.show_frame("PageOne"))
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        # button1.pack()
        # button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Sign Out",
                           command=lambda: controller.show_frame("LoginPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()