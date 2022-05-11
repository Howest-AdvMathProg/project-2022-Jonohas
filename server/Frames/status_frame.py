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

        self.user_table.grid(row=0, column=0, rowspan=3,columnspan=6, sticky=E+W+N+S)

        self.user_table.bind("<<TreeviewSelect>>", self.on_clients_list_select)

        self.user_search_table = ttk.Treeview(self)

        self.user_search_table['columns'] = ('Verb', 'Params')


        self.user_search_table.column("#0", width=0,  stretch=NO)
        self.user_search_table.column("Verb",anchor=W, width=80)
        self.user_search_table.column("Params",anchor=W,width=80)

        self.user_search_table.heading("#0",text="",anchor=W)
        self.user_search_table.heading("Verb",text="Verb",anchor=W)
        self.user_search_table.heading("Params",text="Params",anchor=W)

        self.user_search_table.grid(row=3, column=0, rowspan=3,columnspan=6, sticky=E+W+N+S)


        self.entry_send_broadcast = Entry(self)
        self.entry_send_broadcast.grid(row=4, column=0, columnspan=4, sticky=N+S+E+W)

        self.button_send_broadcast = Button(self, text = "Send client", command=self.send_single_client)
        self.button_send_broadcast.grid(row=4, column=4, sticky=N+S+E+W)

        self.button_send_broadcast = Button(self, text = "Send broadcast", command=self.send_broadcast)
        self.button_send_broadcast.grid(row=4, column=5, sticky=N+S+E+W)

        Grid.columnconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 3, weight=1)

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

        
    def send_single_client(self):
        message_string = self.entry_send_broadcast.get()
        m = ResponseMessage()
        m.verb = "MESSAGE"
        m.body = {
            "sender": "Server",
            "message": message_string
        }
        self.selected_client.send_to_client(m)

    def on_clients_list_select(self, event):

        i = self.user_table.selection()
        try: 
            c = [client for client in self.clients if client.username == i[0]]
            self.selected_client = c[0]

            self.user_search_table.delete(*self.user_search_table.get_children())
            search_history = list(reversed(self.selected_client.search_history))
            for message in search_history:
                print(message.json_string)
                self.user_search_table.insert(parent='',index='end',iid=f"{message.request_verb}_{message.params}",text='',
                    values=(message.request_verb,message.params))

        except Exception as e:
            pass


    def send_message(self, message):
        self.main.send_message(f"StatusFrame: {message}")


    def handle_connected_clients(self):
        while self.main.server._running:
            try:
                clients = self.main.server.client_manager.clients
                self.clients = []
                self.user_table.delete(*self.user_table.get_children())
                for client in clients:
                    if client.is_alive() and client.logged_in:
                        self.clients.append(client)
                        self.user_table.insert(parent='',index='end',iid=f"{client.username}",text='',
                            values=(client.username,client.fullname,client.email))
            except Exception:
                print("Some error occured while adding clients to list")
            time.sleep(1)