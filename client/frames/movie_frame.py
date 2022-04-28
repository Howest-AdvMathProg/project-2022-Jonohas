
from tkinter import *

class MovieFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()

    def init_window(self):
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Single movie tab").grid(row=0)


        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)