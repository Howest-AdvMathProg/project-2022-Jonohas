import json

class Message():
    def __init__(self, verb, endpoint, params):
        self.verb = verb
        self.endpoint = endpoint
        self.params = params

    def __str__(self):
        return json.dumps(self.__dict__(), separators=(',', ':'))

    def __dict__(self):
        return { 'verb': self.verb, 'endpoint': self.endpoint, 'params': self.params}