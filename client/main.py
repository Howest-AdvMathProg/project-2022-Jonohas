
from datetime import datetime
from threading import Thread
from tkinter import *
from tkinter.ttk import Notebook

from frames.movie_frame import MovieFrame
from frames.messages_frame import MessageFrame
from client import Client

from message_handlers.response_message import ResponseMessage
from message_handlers.request_message import RequestMessage

import time


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master
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
        self.messages_frame = MessageFrame(self.notebook, self)

        self.client.connect()
        self.init_window()

        self.server_online = False
        self.heartbeat_last = time.time()

    def init_window(self):
        self.master.title("Movies - Client")
        self.pack(expand=1, fill="both")

        self.server_status_string = StringVar(self.master, "Server status: online")

        self.menubar = Menu(self.master)  
        self.server_tab = Menu(self.menubar, tearoff=0)
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

        self.server_status = Label(self, textvariable=self.server_status_string)
        #self.server_status.grid(row=6, rowspan=1, sticky=S+E+W)

        self.notebook.add(self.movie_frame, text="Movies")
        self.notebook.add(self.messages_frame, text="Messages")
        self.notebook.pack(expand=1, fill="both")

        Grid.columnconfigure(self.top, 1, weight=1)
        Grid.rowconfigure(self.top, 2, weight=1)

        Grid.columnconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 7, weight=1)


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
        self.start_heartbeat()

    def _on_response(self, responseMessage):
        pass
        #print(responseMessage)

    def start_message_listener(self):
        listenerThread = Thread(target=self._handle_incoming_message)
        listenerThread.start()

    def _handle_incoming_message(self):
        while self.message_listener:
            received_message = self.client.receive()
            m = ResponseMessage(received_message, self)

    def start_heartbeat(self):
        heartbeatThread = Thread(target=self._heartbeat)
        heartbeatThread.start()

    def _heartbeat(self):
        self.heartbeat_last = time.time()
        while self.message_listener:
            current_time = time.time()
            if (current_time - self.heartbeat_last > 6):
                self.server_online = False
                if (current_time - self.heartbeat_last > 10):
                    self.message_listener = False

                self.server_status_string.set("Server status: offline")
            else:
                self.server_online = True 

            
            params = {}
            message = RequestMessage('HEARTBEAT', params)
            self.client.send(message)
            time.sleep(2)

    def close(self):
        self.message_listener = False
        self.client.disconnect()
        self.master.destroy()



root = Tk()
root.geometry("900x500")
app = Main(root)
root.protocol("WM_DELETE_WINDOW", app.close)

try:
    root.mainloop()
except KeyboardInterrupt:
    app.close()