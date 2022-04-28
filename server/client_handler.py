from threading import Thread
import logging
from request_message import RequestMessage
from MessageHandlers.message import Message



class ClientHandler(Thread):
    def __init__(self, conn, message_queue):
        Thread.__init__(self)
        self.conn = conn
        self.io = self.conn.makefile(mode='rw')
        self.message_queue = message_queue
        self.name = "UnidentifiedUser-Thread"

        self.logged_in = False

        self.username = ""
        self.fullname = ""
        self.email = ""

    def __iter__(self):
        return self

    def send_to_client(self, string):
        self.io.write(f"{string}\n")
        self.io.flush()

    def receieve_message_client(self):
        value = self.io.readline().rstrip('\n')
        self.io.flush()
        return value

    def send_message(self, message):
        self.message_queue.put(f"{self.name}: {message}")

    def run(self):       
        t = Thread(target=self.start_message_thread)
        t.start()
    
    def start_message_thread(self):
        while True:
            received_message = self.receieve_message_client()
            message = Message(received_message, self)
            mThread = Thread(target=message.run)
            mThread.start()