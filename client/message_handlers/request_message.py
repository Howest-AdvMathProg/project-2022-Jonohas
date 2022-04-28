import json

class RequestMessage():
    def __init__(self, verb, params):
        self.verb = verb
        self.params = params

    def __str__(self):
        return json.dumps(self.__dict__(), separators=(',', ':'))

    def __dict__(self):
        return { 'verb': self.verb, 'params': self.params}