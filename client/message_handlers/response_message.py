import jsonpickle
from eventhandler import EventHandler
import time

class ResponseMessage:

    def __init__(self, jsonString, source):
        self.event_handler = EventHandler('RESPONSE', 'MESSAGE', 'CLOSE', 'HEARTBEAT')
        self.source = source

        if jsonString != "":
            try:
                data = jsonpickle.decode(jsonString)
                self.response_code = data["responseCode"]
                self.verb = data['verb']
                self.body = data["body"]

                self.event_handler.link(self._on_message, 'MESSAGE')
                self.event_handler.link(source._on_response(self), 'RESPONSE')
                self.event_handler.link(self._on_close, 'CLOSE')
                self.event_handler.link(self._on_heartbeat, 'HEARTBEAT')

            except Exception as e:
                print(f"Error: {e}")

            self.event_handler.fire(self.verb)

    def _on_message(self):
        self.source.messages_frame.write_to_text_area(f"{self.body['sender']}: {self.body['message']}")

    def _on_close(self):
        self.client.send_message(f"Finished...")
        self.client.conn.close()

    def _on_heartbeat(self):
        self.source.heartbeat_last = time.time()

    def __str__(self):
        return jsonpickle.encode(self.__dict__(), max_depth=10)

    def __dict__(self):
        return { 'responseCode': self.response_code, 'verb': self.verb, 'body': self.body}
