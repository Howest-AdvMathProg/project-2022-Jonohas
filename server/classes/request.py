
import uuid, jsonpickle

class Request:
    def __init__(self, id, method, params):
        self._id = id
        self._method = method
        self._params = params
        self._count = 0

    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 
            'id': self._id,  
            'method': self._method, 
            'params': self._params
        }

    def __eq__(self, other):
        return self._method == other._method
            