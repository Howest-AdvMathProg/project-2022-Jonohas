
from queue import Queue
from threading import Thread
from classes.response import Response
import jsonpickle

message_queue_send = Queue()
message_queue_receive = Queue()

class ResponseHandler:
    def __init__(self, json_string):
        _response = self.from_string(json_string)
        self._response = Response(_response["id"], _response["code"], _response["method"], _response["result"])
        return self._response

    def from_string(self, string):
        return jsonpickle.decode(string)


    

class ServerCommunication(Thread):
    def __init__(self, io):
        self.io = io
        Thread.__init__(self)

        self._running = True
        self.message_queue_send = Queue()
        self.message_queue_receive = Queue()

    def close(self):
        self._running = False

    def run_send(self):
        global message_queue_send
        while self._running:
            if message_queue_send.not_empty():
                try:
                    self.io.write(f"{message_queue_send.get()}\n")
                    self.io.flush()
                except Exception:
                    pass

    def run(self):
        global message_queue_receive

        while self._running:
            if message_queue_receive.not_empty():
                ResponseHandler(message_queue_receive.get())