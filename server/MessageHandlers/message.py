import json
import jsonpickle
from response_message import ResponseMessage
from eventhandler import EventHandler
from data.repositories.movie_repository import MovieRepository

class Message:

    def __init__(self, jsonString, client, history_queue):
        self.client = client
        self.json_string = jsonString

        self.history_queue = history_queue

        self.response = ResponseMessage()
        
        self.event_handler = EventHandler('LOGIN', 'HEARTBEAT','GET', 'ERROR', 'MESSAGE', 'CLOSE')

        self.event_handler.link(self._on_login, 'LOGIN')
        self.event_handler.link(self._on_heartbeat, 'HEARTBEAT')
        self.event_handler.link(self._on_get, 'GET')
        self.event_handler.link(self._on_error, 'ERROR')
        self.event_handler.link(self._on_message, 'MESSAGE')
        self.event_handler.link(self._on_close, 'CLOSE')

        try:
            data = jsonpickle.decode(jsonString)
            self.request_verb = data['verb']
            self.verb = data['verb']
            self.params = data['params']
        except Exception:
            self.verb = "ERROR"


    def add_to_history(self, message):
        self.history_queue.put(message)
        
    def run(self):
        if self.json_string != "":
            self.event_handler.fire(self.verb)

    def _on_login(self):
        login = self.params
        if (self.valid_login() == True):
            self.client.logged_in = not self.client.logged_in

            self.client.name = f'''{login["username"]}-Thread'''
            self.client.username = login["username"]
            self.client.email = login["email"]
            self.client.fullname = login["fullname"]

            self.response_code = 200
            self.verb = "LOGIN_RESPONSE"

        else:
            self.response_code = 401
            self.verb = "LOGIN_RESPONSE"

        self.client.send_to_client(self.response)

    def _on_heartbeat(self):
        self.response_code = 200
        self.verb = "HEARTBEAT"
        self.body = {}
        self.client.send_to_client(self.response)

    def _on_get(self):
        self.add_to_history(self)
        if (self.params['endpoint'] == "/movies"):
            movie_repository = MovieRepository()
            search_movies = movie_repository.search_by_field(self.params["field"], self.params["value"], self.params["exact"], self.params["sortBy"], self.params["descending"])
            self.client.send_message(f"User requested some data {self.params}")
            self.response_code = 200
            self.verb = "RESPONSE"
            self.body = {
                "movies": search_movies
            }

            self.client.send_to_client(self.response)

        else:
            self.response_code = 200
            self.verb = "RESPONSE"
            self.body = {}

            self.client.send_to_client(self.response)


    def _on_error(self):
        pass

    def _on_message(self):
        pass

    def _on_close(self):
        self.client.message_queue_running = False
        self.client.io.close()
        self.client.conn.close()

    def valid_login(self):
        if self.params["username"] != None and self.params["email"] != None and self.params["fullname"] != None:
            
            self.username = self.params["username"]
            self.email = self.params["email"]
            self.fullname = self.params["fullname"]

            self.response_code = 200
            
            self.body = {
                "valid": True
            }
            return True
        return False

    @property
    def response_code(self):
        return self.response.responseCode

    @response_code.setter
    def response_code(self, code):
        self.response.responseCode = code

    @property
    def body(self):
        return self.response.body

    @body.setter
    def body(self, body):
        self.response.body = body

    @property
    def verb(self):
        return self.response.verb

    @verb.setter
    def verb(self, verb):
        self.response.verb = verb

    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 'verb': self.verb, 'params': self.params}

    def __eq__(self, other):
        return self.request_verb == other.request_verb
