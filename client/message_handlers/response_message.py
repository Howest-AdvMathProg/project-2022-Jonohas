import json
from eventhandler import EventHandler

class ResponseMessage:

    def __init__(self, jsonString):
        
        self.event_handler = EventHandler('RESPONSE', 'MESSAGE', 'CLOSE')

        self.event_handler.link(self._on_message, 'MESSAGE')
        self.event_handler.link(self._on_response, 'RESPONSE')
        self.event_handler.link(self._on_close, 'CLOSE')
        if jsonString != "":
            try:
                data = json.loads(jsonString)
                self.response_code = data["responseCode"]
                self.verb = data['verb']
                self.body = data['body']
            except Exception:
                print("string is not a valid json string")
            self.event_handler.fire(self.verb)

    def _on_message(self):
        print("MESSAGE")

    def _on_response(self):
        print("RESPONSE")

    def _on_close(self):
        self.client.send_message(f"Finished...")
        self.client.conn.close()


    def __str__(self):
        return json.dumps(self.__dict__(), separators=(',', ':'))

    def __dict__(self):
        return { 'verb': self.verb, 'body': self.body}
