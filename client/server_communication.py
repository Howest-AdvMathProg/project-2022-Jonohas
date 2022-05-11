
from threading import Thread

class ServerCommunication(Thread):
    def __init__(self):
        Thread.__init__(self)

        self._running = True


    def close(self):
        self._running = False

    def run(self):
        while self._running:
            print("something")