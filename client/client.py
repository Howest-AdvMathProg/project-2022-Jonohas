import logging
import socket



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

    def connect(self):
        self.client_to_server.connect((self.host, self.port))
        self.io = self.client_to_server.makefile(mode='rw')

    def send(self, string):
        self.io.write(f"{string}\n")
        self.io.flush()

    def receive(self):
        return self.io.readline().rstrip('\n')


client = Client()
client.connect()

# thread for receiving message from server
# thread for handling heartbeat


    #print (message.decode('ascii'))

