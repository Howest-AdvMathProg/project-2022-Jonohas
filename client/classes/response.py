import jsonpickle

class Response:
    def __init__(self, id, code, method, result):
        self.id = id
        self.code = code
        self.method = method
        self.result = result

    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 
            'id': self.id, 
            'code': self.code, 
            'method': self.method, 
            'result': self.result
        }
