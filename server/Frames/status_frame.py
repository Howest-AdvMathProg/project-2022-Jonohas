from tkinter import *
from tkinter import ttk
import time

from response_message import ResponseMessage


class Status(Frame):
    def __init__(self, master=None, main = None):
        Frame.__init__(self,master)
        self.master = master
        self.main = main
        self.init_window()
        
        self.clients = []

    def init_window(self):
        self.pack(expand=1, fill="both")
        self.user_table = ttk.Treeview(self)

        self.user_table['columns'] = ('Username', 'Full name', 'Email')


        self.user_table.column("#0", width=0,  stretch=NO)
        self.user_table.column("Username",anchor=W, width=80)
        self.user_table.column("Full name",anchor=W,width=80)
        self.user_table.column("Email",anchor=W,width=80)

        self.user_table.heading("#0",text="",anchor=W)
        self.user_table.heading("Username",text="Username",anchor=W)
        self.user_table.heading("Full name",text="Full name",anchor=W)
        self.user_table.heading("Email",text="Email",anchor=W)

        self.user_table.grid(row=0, column=0, rowspan=4,columnspan=5, sticky=E+W+N+S)

        self.user_table.bind("<<TreeviewSelect>>", self.on_clients_list_select)

        self.entry_send_broadcast = Entry(self)
        self.entry_send_broadcast.grid(row=4, column=0, columnspan=4, sticky=N+S+E+W)

        self.button_send_broadcast = Button(self, text = "Send broadcast", command=self.send_broadcast)
        self.button_send_broadcast.grid(row=4, column=4, sticky=N+S+E+W)

        Grid.columnconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 2, weight=1)

    def send_broadcast(self):
        message_string = self.entry_send_broadcast.get()
        m = ResponseMessage()
        m.verb = "MESSAGE"
        m.body = {
            "sender": "Server",
            "message": message_string
        }
        for client in self.clients:
            client.send_to_client(m)

    def on_clients_list_select(self, event):

        i = self.user_table.selection()
        try: 
            c = [client for client in self.clients if client.username == i[0]]
            self.selected_client = c[0]
            m = ResponseMessage()
            m.verb = "MESSAGE"
            m.body = {
                "sender": "Server",
                "message": "Server clicked moderator on you!"
            }
            self.selected_client.send_to_client(m)
        except Exception as e:
            pass


    def send_message(self, message):
        self.main.send_message(f"StatusFrame: {message}")


    def handle_connected_clients(self):
        while self.main._running:

            clients = self.main.server.client_manager.clients
            self.clients = []
            self.user_table.delete(*self.user_table.get_children())
            for client in clients:
                if client.is_alive() and client.logged_in:
                    self.clients.append(client)
                    self.user_table.insert(parent='',index='end',iid=f"{client.username}",text='',
                        values=(client.username,client.fullname,client.email))

            time.sleep(1)