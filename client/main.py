from threading import Thread
from tkinter import *
from tkinter.ttk import Notebook

from frames.movie_frame import MovieFrame
from client import Client

from message_handlers.response_message import ResponseMessage
from message_handlers.request_message import RequestMessage


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)

        self.client = Client()

        self.username = ""
        self.fullname = ""
        self.email = ""

        self.top = Toplevel(self)
        self.top.geometry()
        self.top.title("Login")

        self.top.resizable(False,False)



        # setup object for tabbed page
        self.notebook = Notebook(self)

        # frame that serves as tab
        self.movie_frame = MovieFrame(self.notebook)

        self.init_window()

    def init_window(self):
        self.master.title("Movies - Client")
        self.pack(expand=1, fill="both")

        self.notebook.add(self.movie_frame, text="Movies")

        self.username_entry = Entry(self.top)
        self.fullname_entry = Entry(self.top)
        self.email_entry = Entry(self.top)

        Label(self.top, text="Username:").grid(row=0, column=0, pady=(2,5), padx=(2,0))
        Label(self.top, text="Full name:").grid(row=1, column=0, pady=(0,5), padx=(2,0))
        Label(self.top, text="Email:").grid(row=2, column=0, pady=(0,2), padx=(2,0))
        
        self.username_entry.grid(row=0, column=1, sticky=E+W, pady=(2,5), padx=(0,2))
        self.fullname_entry.grid(row=1, column=1, sticky=E+W, pady=(0,5), padx=(0,2))
        self.email_entry.grid(row=2, column=1, sticky=E+W, pady=(0,2), padx=(0,2))

        self.button_login = Button(self.top, text="Login", command=self.login)
        self.button_login.grid(row=3, column=0, columnspan=3, sticky=N+S+E+W)

        self.button_get_movies = Button(self, text="Get movies", command=self.get_movies)
        self.button_get_movies.grid(row=1, column=0, sticky=N+S+E+W)

        Grid.columnconfigure(self.top, 1, weight=1)
        Grid.rowconfigure(self.top, 2, weight=1)

        self.top.wm_transient(self.notebook)

        self.client.connect()


    def login(self):
        self.username = self.username_entry.get()
        self.fullname = self.fullname_entry.get()
        self.email = self.email_entry.get()
        self.master.title(f"Movies - Client - {self.username}")

        params = {
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email
        }
        message = RequestMessage('LOGIN', params)
        self.client.send(message)
        received_message = self.client.receive()
        m = ResponseMessage(received_message)
        if m.response_code == 200:
            self.logged_in = True
            self.top.destroy()


    def get_movies(self):
        params = {}
        message = RequestMessage('GET', params)
        self.client.send(message)
        received_message = self.client.receive()
        m = ResponseMessage(received_message)
        if m.response_code == 200:
            print(m.body)



root = Tk()
root.geometry("900x500")
app = Main(root)
root.mainloop()