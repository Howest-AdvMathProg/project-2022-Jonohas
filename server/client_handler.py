from threading import Thread
import logging

class ClientHandler(Thread):
    def __init__(self, conn, message_queue):
        Thread.__init__(self)
        self.conn = conn
        self.message_queue = message_queue

    def send_message(self, message):
        self.message_queue.put(f"{self.name}: {message}")

    def run(self):
        self.send_message(f"Starting...")

        io_stream_client = self.conn.makefile(mode='rw')
        received_message = io_stream_client.readline().rstrip('\n')
        while received_message != "CLOSE":
            command = received_message.split(":")[0]
            data = received_message.split(':')[1]
            data_values = data.split(';')

            snelheid, reactie_tijd, type_wegdek = data_values

            self.send_message(f"Ontvangen snelheid: {snelheid} km/u")
            self.send_message(f"Ontvangen reactietijd: {reactie_tijd} sec")
            self.send_message(f"Ontvangen type wegdek: {type_wegdek}")

            snelheid_meter_per_seconde = float(snelheid) / 3.6

            snelheid = snelheid_meter_per_seconde
            reactie_tijd = float(reactie_tijd)


            
            if (type_wegdek == 'D'):
                remvertraging = 8
            elif (type_wegdek == 'N'):
                remvertraging = 4
            
            stop_afstand = (snelheid * reactie_tijd) + ((snelheid**2) / (2 * remvertraging))

            io_stream_client.write(f"{stop_afstand}\n")
            io_stream_client.flush()
            self.send_message(f"{stop_afstand}")
            received_message = io_stream_client.readline().rstrip('\n')

        self.conn.close()
        self.send_message(f"Finished...")