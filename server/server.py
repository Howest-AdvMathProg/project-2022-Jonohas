# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
# http://www.techinfected.net/2016/02/make-gui-calculator-in-python-windows-linux.html
import logging
from tkinter import *
from queue import Queue
from threading import Thread
from threading import Event
from server_thread import Server
import socket
import sys
import signal

logging.info("Creating serversocket...")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.init_message_queue()

        self.server = Server(socket.gethostname(), 9999, serversocket, self.message_queue)

        

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.start_stop_text = StringVar()
        self.start_stop_text.set("Start server")
        self.master.title('Server GUI')

        self.pack(fill=BOTH, expand=1)

        Label(self, text="Log-berichten server: ").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.text = Text(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

        self.text.grid(row=1, column=0, sticky=N+S+E+W)
        self.scrollbar.grid(row=1,column=1, sticky=N + S)

        self.start_stop = Button(self, textvariable=self.start_stop_text, width=10, command=lambda: self.start_server())
        self.start_stop.grid(row=2)

        self.stop_start = Button(self, textvariable=self.start_stop_text, width=10, command=lambda: self.stop_server())
        self.stop_start.grid_forget()

        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)


    def write_to_text_area(self):
        while True:
            if self.message_queue.not_empty:
                self.text['state'] = 'normal'
                self.text.insert(END, f"{self.message_queue.get()}\n")
                self.text['state'] = 'disabled'

    def signal_handler(self, signum, frame):
        self.server.exit_event.set()

    def start_server(self):
        self.message_queue.put(f"Starting server...")
        self.server.start()
        self.start_stop_text.set("Stop server")
        self.start_stop.grid_forget()
        self.stop_start.grid(row=2)

        self.server.join()

    def stop_server(self):
        self.message_queue.put(f"Closing server...")
        self.server.close()
        
        

    def init_message_queue(self):
        self.message_queue = Queue()
        t = Thread(target=self.write_to_text_area)
        t.start()


root = Tk()
root.geometry("500x300")
app = Window(root)
signal.signal(signal.SIGINT, app.signal_handler)
root.mainloop()
