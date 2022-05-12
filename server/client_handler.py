from threading import Thread
import logging
from client_communication import ClientCommunication
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

        self.client_comm = ClientCommunication(self.io, self)
        self.client_comm.start()

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

    def send(self, string):
        self.client_comm.send(string)

    def close(self):
        self._running = False
        self.client_comm.close()
        self.conn.close()


    def run(self):       
        while self._running:
            pass

            # message = Message(received_message, self, self.history_queue)
            # self.search_history.append(message)
            # mThread = Thread(target=message.run)
            # mThread.start()
        self.send_message("I'm closing!")
        


