import logging
import threading
import socket

from client_handler import ClientHandler
from client_manager import ClientManager

class Server(threading.Thread):
    def __init__(self, host, port, socket, message_queue):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = socket
        self.name = "Server-Thread"
        self.message_queue = message_queue
        self.send_message(f"Server initilized")

        try:
        # bind to the port
            self.socket.bind((self.host, self.port))
            self.send_message(f"Starting server...")
        except Exception as e:
            self.send_message("Failed to bind to port")

        # queue up to 20 requests
        self.socket.listen(20)
        self._running = True

        self.client_manager = ClientManager()

    def send_message(self, message):
        self.message_queue.put(f"{self.name}: {message}")

    def close(self):
        self.send_message("Closing...")
        self._running = False
        socket.socket(socket.AF_INET, 
            socket.SOCK_STREAM).connect( (self.host, self.port))

        self.client_manager.close_clients()
        self.socket.close()

    def run(self):
        while self._running == True:
            try:
                conn, addr = self.socket.accept()
                if self._running:
                    self.send_message(f"Client connected: {addr}")
                self.client_manager.add_client(conn, self.message_queue)

            except KeyboardInterrupt:
                self.close()
                print("Caught keyboard interrupt, exiting")
                break


