import json

class MessageHandler():
    def __init__(self, jsonString):
        data = json.loads(jsonString)
        print(data)
        self.verb = data['verb']
        self.endpoint = data['endpoint']
        self.params = data['params']

    def __str__(self):
        return json.dumps(self.__dict__(), separators=(',', ':'))

    def __dict__(self):
        return { 'verb': self.verb, 'endpoint': self.endpoint, 'params': self.params}