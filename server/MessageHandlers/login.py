

from MessageHandlers.message import Message


class Login(Message):
    def __init__(self, message_queue, io_stream_client, message):
        super().__init__(message_queue, io_stream_client, message)
        
        self.valid = False
        self.valid_login()

    def valid_login(self):
        if self.message.params["username"] != None and self.message.params["email"] != None and self.message.params["fullname"] != None:
            
            self.username = self.message.params["username"]
            self.email = self.message.params["email"]
            self.fullname = self.message.params["fullname"]

            self.response.responseCode = 200

            self.response.body = {
                "valid": True
            }
            self.valid = True
        else:
            self.valid = False
            