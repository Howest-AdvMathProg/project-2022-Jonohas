
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

        self.message_listener = True

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
        self.movie_frame = MovieFrame(self.notebook, self)
        self.client.connect()
        self.init_window()

    def init_window(self):
        self.master.title("Movies - Client")
        self.pack(expand=1, fill="both")

        self.menubar = Menu(self.master)  
        self.server_tab = Menu(self.menubar, tearoff=1)   
        self.server_tab.add_command(label="Disconnect", command=self.client.disconnect)
        self.menubar.add_cascade(label="Server", menu=self.server_tab) 

        self.master.config(menu=self.menubar) 

        
        ### LOGIN
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
        ### LOGIN


        self.notebook.add(self.movie_frame, text="Movies")
        self.notebook.pack(expand=1, fill="both")

        Grid.columnconfigure(self.top, 1, weight=1)
        Grid.rowconfigure(self.top, 2, weight=1)
        self.top.wm_transient(self.notebook)

        


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
        m = ResponseMessage(received_message, self)
        if m.response_code == 200:
            self.logged_in = True
            self.top.destroy()


            params = {
                "field": "title",
                "value": "Spider-Man",
                "exact": False,
                "sortBy": "releaseDate",
                "descending": False
            }
            self.movie_frame.get_movies(params)

            self.start_message_listener()

    def _on_response(self, responseMessage):
        print(responseMessage)

    def start_message_listener(self):
        listenerThread = Thread(target=self._handle_incoming_message)
        listenerThread.start()

    def _handle_incoming_message(self):
        while self.message_listener:
            received_message = self.client.receive()
            m = ResponseMessage(received_message, self)








root = Tk()
root.geometry("900x500")
app = Main(root)
root.mainloop()
    