

from re import L
from threading import Thread
from tkinter import *
from tkinter import ttk
import time

class PopularSearch(Frame):
    def __init__(self, master=None, main = None):
        Frame.__init__(self,master)
        self.master = master
        self.main = main
        self.init_window()
        self._running = True


        self.history_queue = main.history_queue

        self._search_history = []

    def start_history_queue_handler(self):
        self.history_queue_handler = Thread(target=self.handle_history_queue)
        self.history_queue_handler.start()

    def handle_history_queue(self):
        while self._running:
            if self.history_queue.not_empty:
                try:
                    self._search_history.append(self.history_queue.get())
                    
                except Exception:
                    pass

                self.update_history_table()
                
            time.sleep(1)

    def update_history_table(self):
        self.history_search_table.delete(*self.history_search_table.get_children())
        for message in self._search_history:
            print(message.json_string)
            self.history_search_table.insert(parent='',index='end',iid=f"{message.request_verb}_{message.params}",text='',
                values=(message.request_verb,message.params, 0))


    def init_window(self):

        self.pack(fill=BOTH, expand=1)

        Label(self, text="Log-berichten server: ").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.text = Text(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

        self.history_search_table = ttk.Treeview(self)

        self.history_search_table['columns'] = ('Verb', 'Params', 'Count')

        self.history_search_table.column("#0", width=0,  stretch=NO)
        self.history_search_table.column("Verb",anchor=W, width=10)
        self.history_search_table.column("Params",anchor=W,width=80)
        self.history_search_table.column("Count",anchor=W,width=10)

        self.history_search_table.heading("#0",text="",anchor=W)
        self.history_search_table.heading("Verb",text="Verb",anchor=W)
        self.history_search_table.heading("Params",text="Params",anchor=W)
        self.history_search_table.heading("Count",text="Count",anchor=W)

        self.history_search_table.grid(row=0, column=0, rowspan=3,columnspan=6, sticky=E+W+N+S)

        self.text.grid(row=1, column=0, sticky=N+S+E+W)
        self.scrollbar.grid(row=1,column=1, sticky=N + S)

        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

    def send_message(self):
        print("pressed!")