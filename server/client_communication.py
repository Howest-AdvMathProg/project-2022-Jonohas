
import json
from queue import Queue
from threading import Thread
from classes.request import Request
from classes.response import Response
from eventhandler import EventHandler
import jsonpickle

from data.repositories.movie_repository import MovieRepository

message_queue_send = Queue()
message_queue_receive = Queue()


class PrivateData:
    def __init__(self, response):
        self._response = response

class PublicData:
    def __init__(self, request, client):
        self.client = client
        self._request = request
        self.event_handler = EventHandler('get-movies', 'login', 'heartbeat', 'close', 'graph')

        self.event_handler.link(self._get_movies, 'get-movies')
        self.event_handler.link(self._login, 'login')
        self.event_handler.link(self._heartbeat, 'heartbeat')
        self.event_handler.link(self._close, 'close')
        self.event_handler.link(self._graph, 'graph')

        method = self._request._method.split('/')[1]
        self.event_handler.fire(method)

    def _get_movies(self):
        mr = MovieRepository()
        params = self._request._params
        movies = mr.search_by_field(params['field'], params['value'], params['exact'], params['sortBy'], params['descending'])
        self.client.send(Response(self._request._id, 200, self._request._method, { "movies": movies }))
        self.client.search_history.append(self._request)

    def _login(self):
        self.client.send(Response(self._request._id, 200, self._request._method, { "valid": True }))
        self.client.username = self._request._params['username']
        self.client.fullname = self._request._params['fullname']
        self.client.email = self._request._params['email']
        self.client.name = f"{self.client.username}-Thread"
        self.client.logged_in = True
        self.client.search_history.append(self._request)


    def _heartbeat(self):
        self.client.send(Response(self._request._id, 200, self._request._method, {}))

    def _close(self):
        self.client.close()

    def _graph(self):
        pass

class RequestHandler:
    def __init__(self, json_string, client):

        self.client = client

        

        _request = self.from_string(json_string)
        self._request = Request(_request["id"], _request["method"], _request["params"])

        

        method = self._request._method.split('/')[0]
        if method == "public":
            PublicData(self._request, self.client)
        

    def from_string(self, string):
        return jsonpickle.decode(string)
    

class ClientCommunication(Thread):
    def __init__(self, io, client):
        self.client = client
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

    def send(self, object):
        self.message_queue_send.put(object)

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
                RequestHandler(self.message_queue_receive.get(), self.client)