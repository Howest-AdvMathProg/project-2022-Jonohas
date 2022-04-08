from threading import Thread
import logging
from message_handler import MessageHandler

class ClientHandler(Thread):
    def __init__(self, conn, message_queue):
        Thread.__init__(self)
        self.conn = conn
        self.message_queue = message_queue

    def send_message(self, message):
        self.message_queue.put(f"{self.name}: {message}")

    def run(self):
        self.send_message(f"Starting...")

        io_stream_client = self.conn.makefile(mode='rw')
        received_message = io_stream_client.readline().rstrip('\n')
        message = MessageHandler(received_message)
        while message.verb != "CLOSE":
            self.send_message(f"Message received: {message.verb} requested data: {message.endpoint}, request params: {message.params}")

            io_stream_client.write(f"{message}\n")
            io_stream_client.flush()
            received_message = io_stream_client.readline().rstrip('\n')
            message = MessageHandler(received_message)

        self.send_message(f"Finished...")
        self.conn.close()