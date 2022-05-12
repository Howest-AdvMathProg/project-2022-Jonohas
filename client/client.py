import logging
import socket
from server_communication import ServerCommunication
from classes.request import Request

logging.basicConfig(level=logging.INFO)

socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client:
    def __init__(self, main):
        self._main = main
        self.client_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info("Making connection with server...")

        self.logged_in = False

        # get local machine name
        self.host = socket.gethostname()
        self.port = 9999

        self.ser_com = None


    def connect(self):
        self.client_to_server.connect((self.host, self.port))
        self.io = self.client_to_server.makefile(mode='rw')
        self.ser_com = ServerCommunication(self.io, self._main)
        self.ser_com.start()

    def send(self, dict):
        self.ser_com.message_queue_send.put(dict)

    def disconnect(self):
        message = Request('public/close', {})
        self.send(message)
        self.ser_com._running = False
        self.client_to_server.close()


