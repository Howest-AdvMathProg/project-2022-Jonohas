from response_message import ResponseMessage

class Message:

    def __init__(self, message_queue, io_stream_client, message):
        
        self.message_queue = message_queue
        self.io = io_stream_client
        self.message = message

        self.response = ResponseMessage()

    def send_message_(self, string):
        self.message_queue.put(f"{string}")

    def send_to_client(self, string):
        self.io.write(f"{string}\n")
        self.io.flush()

    @property
    def response_code(self):
        return self.response.responseCode

    @response_code.setter
    def response_code(self, code):
        self.response.responseCode = code

    @property
    def body(self):
        return self.response.body

    @body.setter
    def body(self, body):
        self.response.body = body

