import logging
import socket
from typing import final


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
            snelheid = input("Send to server, snelheid: ")
            reactietijd = input("Send to server, reactietijd: ")
            type_wegdek = input("Send to server, type wegdek: ")

            message = f"data:{snelheid};{reactietijd};{type_wegdek}"
            io_stream_server.write(f"{message}\n")
            io_stream_server.flush()
            received_command = input('Command ( data or CLOSE ): ')
        
        io_stream_server.write(f"{received_command}\n")
        io_stream_server.flush()
        socket_to_server.close()
        break

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        break


    #print (message.decode('ascii'))

