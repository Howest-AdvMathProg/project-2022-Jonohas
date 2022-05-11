import logging
import socket
from client.server_communication import ServerCommunication


from message_handlers.request_message import RequestMessage
logging.basicConfig(level=logging.INFO)

socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client:
    def __init__(self):
        self.client_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info("Making connection with server...")

        self.logged_in = False

        # get local machine name
        self.host = socket.gethostname()
        self.port = 9999

        self.io = None
        self.ser_com = None


    def connect(self):
        self.client_to_server.connect((self.host, self.port))
        self.io = self.client_to_server.makefile(mode='rw')
        self.ser_com = ServerCommunication(self.io) 


     

    def send(self, string):
        self.ser_com.send
        try:
            self.io.write(f"{string}\n")
            self.io.flush()
        except Exception:
            pass

    def receive(self):
        return self.io.readline().rstrip('\n')

    def disconnect(self):
        message = RequestMessage('CLOSE', {})
        self.send(message)
        self.client_to_server.close()


