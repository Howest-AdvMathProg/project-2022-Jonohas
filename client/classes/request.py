
import uuid, jsonpickle

class Request:
    def __init__(self, method, params):
        self.id = uuid.uuid4().hex
        self.method = method
        self.params = params

    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 
            'id': self.id,  
            'method': self.method, 
            'params': self.params
        }