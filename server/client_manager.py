

from client_handler import ClientHandler

class ClientManager():
    
    def __init__(self):
        self._clients = []


    def add_client(self, conn, message_queue):
        clh = ClientHandler(conn, message_queue)
        self._clients.append(clh)
        clh.start()


    @property
    def clients(self):
        return self._clients

