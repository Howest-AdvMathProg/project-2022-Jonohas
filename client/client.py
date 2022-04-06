import logging
import socket
from typing import final
from message import Message


logging.basicConfig(level=logging.INFO)

logging.info("Making connection with server...")

# create a socket object
socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999

# connection to hostname on the port.
socket_to_server.connect((host, port))
while True:
    try:
        io_stream_server = socket_to_server.makefile(mode='rw')
        received_command = input('Command ( data or CLOSE ): ')

        while received_command != "CLOSE":

            params = {
                'name': 'Jonas'
            }

            message = Message('GET', '/api/v1', params)
            print(message)
            io_stream_server.write(f"{message}\n")
            io_stream_server.flush()
            received_command = input('Command ( data or CLOSE ): ')

        params = {
            
        }

        message = Message('CLOSE', '/', params)
        
        io_stream_server.write(f"{message}\n")
        io_stream_server.flush()
        socket_to_server.close()
        break

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        break


    #print (message.decode('ascii'))

