
import json
from queue import Queue
from threading import Thread
from classes.response import Response
from eventhandler import EventHandler
import jsonpickle
import time

message_queue_send = Queue()
message_queue_receive = Queue()


class PrivateData:
    def __init__(self, response):
        self._response = response

class PublicData:
    def __init__(self, response, main):
        self._main = main
        self._response = response
        self.event_handler = EventHandler('get-movies', 'login', 'heartbeat', 'message')

        self.event_handler.link(self._get_movies, 'get-movies')
        self.event_handler.link(self._login, 'login')
        self.event_handler.link(self._heartbeat, 'heartbeat')
        self.event_handler.link(self._message, 'message')

        
        method = self._response._method.split('/')[1]
        self.event_handler.fire(method)

    def _get_movies(self):
        self._main.movie_frame.fill_movies(self._response._result['movies'])

    def _login(self):
        # close login window request movie data
        if self._response._code == 200:
            self._main.username = self._main.username_entry.get()
            self._main.fullname = self._main.fullname_entry.get()
            self._main.email = self._main.email_entry.get()

            self._main.top.destroy()

            params = {
                "field": "title",
                "value": "Spider-Man",
                "exact": False,
                "sortBy": "releaseDate",
                "descending": False
            }
            self._main.movie_frame.get_movies(params)

    def _heartbeat(self):
        self._main.heartbeat_last = time.time()

    def _message(self):
        sender = self._response._result['sender']
        message = self._response._result['message']
        self._main.messages_frame.write_to_text_area(f"{sender}: {message}")
        

class ResponseHandler:
    def __init__(self, json_string, main):
        self._main = main
        _response = self.from_string(json_string)
        self._response = Response(_response["id"], _response["code"], _response["method"], _response["result"])

        method = self._response._method.split('/')[0]
        if method == "public":
            PublicData(self._response, self._main)
        

    def from_string(self, string):
        return jsonpickle.decode(string)
    

class ServerCommunication(Thread):
    def __init__(self, io, main):
        self._main = main
        self.io = io
        Thread.__init__(self)

        self._running = True

        self.message_queue_send = Queue()
        self.message_queue_receive = Queue()

        send_thread = Thread(target=self.run_send)
        send_thread.start()

        receive_thread = Thread(target=self.run_receive)
        receive_thread.start()

    def close(self):
        self._running = False

    def run_send(self):
        while self._running:
            if self.message_queue_send.not_empty:
                try:
                    self.io.write(f"{self.message_queue_send.get()}\n")
                    self.io.flush()
                except Exception:
                    pass

    def run_receive(self):
        while self._running:
            try:
                value = self.io.readline().rstrip('\n')
                self.message_queue_receive.put(value)
            except Exception:
                pass

    def run(self):
        while self._running:
            if self.message_queue_receive.not_empty:
                ResponseHandler(self.message_queue_receive.get(), self._main)