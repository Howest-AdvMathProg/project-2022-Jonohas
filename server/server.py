# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
# http://www.techinfected.net/2016/02/make-gui-calculator-in-python-windows-linux.html
import logging
from tkinter import *
from tkinter.ttk import Notebook
from queue import Queue
from threading import Thread
from server_thread import Server
import socket
import time

from Frames.log_frame import Log
from Frames.status_frame import Status

logging.info("Creating serversocket...")



class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self._running = True
        self.app = Notebook(self)

        self.history_queue = Queue()

        self.status_screen = Status(self.app, self)
        self.log_screen = Log(self.app, self)

        self.init_message_queue()
        self.init_window()
        

    def init_window(self):
        self.master.title("Movies - Moderator")
        self.pack(expand=1, fill="both")

        self.menubar = Menu(self.master)  
        self.server_tab = Menu(self.menubar, tearoff=0)   
        self.server_tab.add_command(label="Start server", command=self.start_server)  
        self.server_tab.add_command(label="Stop server", command=self.stop_server)  
        self.menubar.add_cascade(label="Server", menu=self.server_tab) 

        self.master.config(menu=self.menubar) 

        self.app.add(self.log_screen, text="Log")
        self.app.add(self.status_screen, text="Status")
        self.app.pack(expand=1, fill="both")

    def start_server(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = Server(socket.gethostname(), 9999, serversocket, self.message_queue, self.history_queue)
        self.server.start()

        t = Thread(target=self.status_screen.handle_connected_clients)
        t.start()

    def stop_server(self):
        try:
            self.server.close()
        except Exception as e:
            print(e)

    def init_message_queue(self):
        self.message_queue = Queue()
        t = Thread(target=self.log_screen.write_to_text_area)
        t.start()

    def send_message(self, message):
        self.message_queue.put(message)

    def on_closing(self):
        self._running = False
        self.stop_server()
        self.destroy()


root = Tk()
root.geometry("600x400")

app = Main(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)


try:
    root.mainloop()
except KeyboardInterrupt:
    app.on_closing()
