# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
# http://www.techinfected.net/2016/02/make-gui-calculator-in-python-windows-linux.html
import logging
from tkinter import *
from queue import Queue
from threading import Thread
from server_thread import Server
import socket

logging.info("Creating serversocket...")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.init_message_queue()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title('Server GUI')

        self.pack(fill=BOTH, expand=1)

        Label(self, text="Log-berichten server: ").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.text = Text(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

        self.text.grid(row=1, column=0, sticky=N+S+E+W)
        self.scrollbar.grid(row=1,column=1, sticky=N + S)

        self.start_stop = Button(self, text="Start server", width=10, command=lambda: self.start_server()).grid(row=2)

        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)


    def write_to_text_area(self):
        while True:
            if self.message_queue.not_empty:
                self.text['state'] = 'normal'
                self.text.insert(END, f"{self.message_queue.get()}\n")
                self.text['state'] = 'disabled'

    def start_server(self):
        self.server = Server(socket.gethostname(), 9999, serversocket, self.message_queue)
        self.server.start()

    def stop_server(self):
        self.message_queue.put(f"Closing server")
        self.server.close()

    def init_message_queue(self):
        self.message_queue = Queue()
        t = Thread(target=self.write_to_text_area)
        t.start()


root = Tk()
root.geometry("500x300")
app = Window(root)
root.mainloop()
