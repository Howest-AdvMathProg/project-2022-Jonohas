from threading import Thread
import logging
from request_message import RequestMessage
from MessageHandlers.data import Data
from MessageHandlers.login import Login

class ClientHandler(Thread):
    def __init__(self, conn, message_queue):
        Thread.__init__(self)
        self.conn = conn
        self.message_queue = message_queue
        self.name = "UnidentifiedUser-Thread"

        self.logged_in = False

        self.username = ""
        self.fullnane = ""
        self.email = ""

    def send_message(self, message):
        self.message_queue.put(f"{self.name}: {message}")

    def run(self):
        self.send_message(f"Starting...")

        io_stream_client = self.conn.makefile(mode='rw')
        received_message = io_stream_client.readline().rstrip('\n')
        message = RequestMessage(received_message)
        while message.verb != "CLOSE":

            # Handle the login function
            if message.verb == "POST" and message.endpoint == "/api/v1/login":
                login = Login(self.message_queue, io_stream_client, message)
                if (login.valid == True):
                    self.logged_in = not self.logged_in
                    self.name = f"{login.username}-Thread"
                    self.username = login.username
                    self.email = login.email
                    self.fullname = login.fullname
                login.send_to_client(login.response)
            
            # Handle all other queries
            if (message.verb == "GET" and self.logged_in == True):
                data = Data(message_queue=self.message_queue, io_stream_client=io_stream_client, message=message)
                data.send_to_client(data.response)

            received_message = io_stream_client.readline().rstrip('\n')
            message = RequestMessage(received_message)

        self.send_message(f"Finished...")
        self.conn.close()