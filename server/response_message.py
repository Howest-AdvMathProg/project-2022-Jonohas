import json

class ResponseMessage():
    def __init__(self):
        self.responseCode = None
        self.verb = None
        self.body = None

    def __str__(self):
        return json.dumps(self.__dict__(), separators=(',', ':'))

    def __dict__(self):
        return { 'responseCode': self.responseCode, 'verb': self.verb, 'body': self.body}