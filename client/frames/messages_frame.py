

from re import L
from tkinter import *

class MessageFrame(Frame):
    def __init__(self, master=None, main = None):
        Frame.__init__(self,master)
        self.master = master
        self.main = main
        self.init_window()
        self._running = True


    def write_to_text_area(self, text):
        self.text['state'] = 'normal'
        self.text.insert(END, f"{text}\n")
        self.text['state'] = 'disabled'

    def init_window(self):
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Berichten van server: ").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.text = Text(self, yscrollcommand=self.scrollbar.set)
        self.text['state'] = 'disabled'
        self.scrollbar.config(command=self.text.yview)

        self.text.grid(row=1, column=0, sticky=N+S+E+W)
        self.scrollbar.grid(row=1,column=1, sticky=N + S)

        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
