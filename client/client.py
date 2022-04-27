from http.client import IncompleteRead
import logging
import socket
from typing import final
from message import Message
from message_handler import MessageHandler
from response_message import ResponseMessage


logging.basicConfig(level=logging.INFO)

logging.info("Making connection with server...")

logged_in = False

# create a socket object
socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999

# connection to hostname on the port.
socket_to_server.connect((host, port))
while True:
    try:
        received_command = "login"
        io_stream_server = socket_to_server.makefile(mode='rw')
        while received_command != "CLOSE":
            if (logged_in):
                params = {
                    'name': 'Jonas'
                }

                message = Message('GET', '/api/v1', params)
                print(f"Sending message: {message}")
                io_stream_server.write(f"{message}\n")
                io_stream_server.flush()
                received_message = io_stream_server.readline().rstrip('\n')
                print(f"Received messsage: {received_message}")
                m = ResponseMessage(received_message)
                print(f"Received converted to ResponseMessage: {m}")
                received_command = input('Command ( data or CLOSE ): ')

            else:
                username = "Jonahas"
                email = "jonas.h.faber@gmail.com"
                fullname = "Jonas Faber"

                params = {
                    "username": username,
                    "email": email,
                    "fullname": fullname
                }
                message = Message('POST', '/api/v1/login', params)

                io_stream_server.write(f"{message}\n")
                io_stream_server.flush()
                received_message = io_stream_server.readline().rstrip('\n')
                m = ResponseMessage(received_message)
                if m.body["valid"] == True:
                    logged_in = True
                    received_command = input('Command ( data or CLOSE ): ')

                else:
                    received_command = "login"


        params = {
            
        }

        message = Message('CLOSE', '/', params)
        
        io_stream_server.write(f"{message}\n")
        io_stream_server.flush()
        socket_to_server.close()
        break

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        socket_to_server.close()
        break


    #print (message.decode('ascii'))

