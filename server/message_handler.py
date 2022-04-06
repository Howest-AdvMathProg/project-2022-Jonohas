import json

class MessageHandler():
    def __init__(self, message):
        self.message = json.loads(message)
        self.verb = self.message["verb"]
        self.endpoint = self.message["endpoint"]
        self.params = self.message["params"]
