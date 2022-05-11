import jsonpickle

class Response:
    def __init__(self, id, code, method, result):
        self._id = id
        self._code = code
        self._method = method
        self._result = result

    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 
            'id': self._id, 
            'code': self._code, 
            'method': self._method, 
            'result': self._result
        }
