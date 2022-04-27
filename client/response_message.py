import json

class ResponseMessage():
    def __init__(self, jsonString):

        data = json.loads(jsonString)
        self.responseCode = data["responseCode"]
        self.body = data["body"]

    def __str__(self):
        return json.dumps(self.__dict__(), separators=(',', ':'))

    def __dict__(self):
        return { 'reponseCode': self.responseCode, 'body': self.body}