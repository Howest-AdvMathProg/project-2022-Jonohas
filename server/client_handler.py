from threading import Thread
import logging
from request_message import RequestMessage
from MessageHandlers.message import Message
import socket



class ClientHandler(Thread):
    def __init__(self, conn, message_queue, history_queue):
        Thread.__init__(self)
        self.conn = conn
        self.io = self.conn.makefile(mode='rw')
        self.message_queue = message_queue
        self.name = "UnidentifiedUser-Thread"

        self.history_queue = history_queue

        self._running = True

        self.logged_in = False

        self.username = ""
        self.fullname = ""
        self.email = ""
        self.search_history = []

    def __iter__(self):
        return self

    def is_socket_closed(self) -> bool:
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = self.conn.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True

        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            return False
        return False

    def send_message(self, message):
        self.message_queue.put(f"{self.name}: {message}")

    def send_to_client(self, string):
        self.io.write(f"{string}\n")
        self.io.flush()

    def receieve_message_client(self):
        if self.is_socket_closed():
            self._running = False

        try:
            value = self.io.readline().rstrip('\n')
            return value
        except Exception:
            self._running = False

    def close(self):
        self._running = False
        self.conn.close()


    def run(self):       
        while self._running:
            received_message = self.receieve_message_client()
            message = Message(received_message, self, self.history_queue)
            self.search_history.append(message)
            mThread = Thread(target=message.run)
            mThread.start()
        self.send_message("I'm closing!")
        


