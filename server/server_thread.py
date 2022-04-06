import logging
import threading

from client_handler import ClientHandler

class Server(threading.Thread):
    def __init__(self, host, port, socket, message_queue):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = socket
        self.name = "Server-Thread"
        self.message_queue = message_queue
        # bind to the port
        self.socket.bind((self.host, self.port))

        # queue up to 5 requests
        self.socket.listen(20)


    def send_message(self, message):
        self.message_queue.put(f"{self.name}: {message}")

    def run(self):
        while True:
            self.send_message(f"Server starting...")
            conn, addr = self.socket.accept()
            self.send_message(f"Client connected: {addr}")
            clh = ClientHandler(conn, self.message_queue)
            clh.start()