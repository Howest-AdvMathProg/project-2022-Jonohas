import json
from response_message import ResponseMessage
from eventhandler import EventHandler
from data.repositories.movie_repository import MovieRepository

class Message:

    def __init__(self, jsonString, client):
        self.client = client
        self.client.send_message(f"Starting...")

        self.response = ResponseMessage()
        
        self.event_handler = EventHandler('LOGIN', 'GET', 'ERROR', 'MESSAGE', 'CLOSE')

        self.event_handler.link(self._on_login, 'LOGIN')
        self.event_handler.link(self._on_get, 'GET')
        self.event_handler.link(self._on_error, 'ERROR')
        self.event_handler.link(self._on_message, 'MESSAGE')
        self.event_handler.link(self._on_close, 'CLOSE')

        if jsonString != "":
            try:
                data = json.loads(jsonString)
                self.verb = data['verb']
                self.params = data['params']
            except Exception:
                self.verb = "ERROR"


            


    def run(self):
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
            self.verb = "RESPONSE"

        else:
            self.response_code = 401
            self.verb = "RESPONSE"

        print(self.response)
        self.client.send_to_client(self.response)

    def _on_get(self):
        movie_repository = MovieRepository()
        self.response_code = 200
        self.verb = "RESPONSE"
        self.body = {
            "movies": movie_repository.movie_list
        }
        self.client.send_to_client(self.response)


    def _on_error(self):
        print("error")

    def _on_message(self):
        print("message")

    def _on_close(self):
        self.client.send_message(f"Finished...")
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
        return json.dumps(self.__dict__(), separators=(',', ':'))

    def __dict__(self):
        return { 'verb': self.verb, 'params': self.params}
