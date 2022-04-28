from tkinter import *
import time


class Status(Frame):
    def __init__(self, master=None, main = None):
        Frame.__init__(self,master)
        self.master = master
        self.main = main
        self.init_window()
        
        self.clients = []



    def init_window(self):
        self.pack(expand=1, fill="both")
        self.selected_client = StringVar()
        self.selected_client.set("empty")

        self.username_label = Label(self, textvariable=self.selected_client).grid(row=0, column=0, sticky=E+W)
        self.client_list = Listbox(self)
        self.client_list.grid(row=1, column=0, rowspan=4, sticky=E+W)

        self.client_list.bind("<<ListboxSelect>>", self.on_clients_list_select)

    def on_clients_list_select(self, event):
        i = self.client_list.curselection()[0]
        client = self.clients[i]

        self.main.add_message_queue(client)
        self.selected_client.set(self.client_list.get(i))



    def send_message(self):
        print("pressed!")


    def handle_connected_clients(self):
        while self.main._running:
            clients = self.main.server.client_manager.clients
            self.clients = []
            self.client_list.delete(0, END)
            for client in clients:
                if client.is_alive() and client.logged_in:
                    self.clients.append(client)
                    self.client_list.insert(END, client.username)

            time.sleep(1)