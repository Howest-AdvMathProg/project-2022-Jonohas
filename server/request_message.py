import jsonpickle

class RequestMessage():
    def __init__(self, jsonString):

        try:
            data = jsonpickle.decode(jsonString)
            self.verb = data['verb']
            self.endpoint = data['endpoint']
            self.params = data['params']
        except Exception:
            print("string is not a valid json string")
            self.verb = "CLOSE"


    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 'verb': self.verb, 'endpoint': self.endpoint, 'params': self.params}