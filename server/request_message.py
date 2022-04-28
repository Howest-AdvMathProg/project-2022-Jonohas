import json

class RequestMessage():
    def __init__(self, jsonString):

        try:
            data = json.loads(jsonString)
            self.verb = data['verb']
            self.endpoint = data['endpoint']
            self.params = data['params']
        except Exception:
            print("string is not a valid json string")
            self.verb = "CLOSE"


    def __str__(self):
        return json.dumps(self.__dict__(), separators=(',', ':'))

    def __dict__(self):
        return { 'verb': self.verb, 'endpoint': self.endpoint, 'params': self.params}