import jsonpickle

class ResponseMessage():
    def __init__(self):
        self.responseCode = None
        self.verb = None
        self.body = None

    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 'responseCode': self.responseCode, 'verb': self.verb, 'body': self.body}