

from client_handler import ClientHandler

class ClientManager():
    
    def __init__(self, history_queue):
        self._clients = []
        self.history_queue = history_queue


    def add_client(self, conn, message_queue):
        clh = ClientHandler(conn, message_queue, self.history_queue)
        self._clients.append(clh)
        clh.start()

    def close_clients(self):
        for client in self._clients:
            client.close()


    @property
    def clients(self):
        return self._clients

