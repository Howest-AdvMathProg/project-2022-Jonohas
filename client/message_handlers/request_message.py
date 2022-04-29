import json

import jsonpickle

class RequestMessage():
    def __init__(self, verb, params):
        self.verb = verb
        self.params = params

    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 'verb': self.verb, 'params': self.params}