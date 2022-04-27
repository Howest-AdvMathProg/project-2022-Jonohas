# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
# http://www.techinfected.net/2016/02/make-gui-calculator-in-python-windows-linux.html
import logging
from tkinter import *
from queue import Queue
from threading import Thread
from threading import Event
from data.repositories.movie_repository import MovieRepository
from server_thread import Server
import socket
import sys
import signal

logging.info("Creating serversocket...")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Main():
    def __init__(self):
        self._running = True
        self.init_message_queue()
        self.server = Server(socket.gethostname(), 9999, serversocket, self.message_queue)

    def write_to_text_area(self):
        while self._running:
            if self.message_queue.not_empty:
                print(f"{self.message_queue.get()}\n")

    def start_server(self):
        self.message_queue.put(f"Starting server...")
        self.server.start()

    def stop_server(self):
        self.message_queue.put(f"Closing server...")
        self.server.close()
        self._running = False

    def init_message_queue(self):
        self.message_queue = Queue()
        t = Thread(target=self.write_to_text_area)
        t.start()



app = Main()
app.start_server()
