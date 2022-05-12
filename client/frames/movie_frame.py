
from sqlite3 import Row
from tkinter import *
from tkinter import ttk
from urllib.request import Request, urlopen
from PIL import Image, ImageTk
import ssl
import base64
from io import BytesIO

from classes.request import Request

import os, glob

import requests
import shutil
from os.path import exists
ssl._create_default_https_context = ssl._create_unverified_context

from threading import Thread

def getImageFromURL(url, controller, filename):
    try:
        res = requests.get(url, stream = True)
        if res.status_code == 200:
            

            file_exists = exists(filename)
            if not file_exists:
                with open(filename,'wb') as f:
                    shutil.copyfileobj(res.raw, f)
        else:
            raise 'Image Couldn\'t be retrieved'


        im = Image.open(filename).resize((200,300), Image.ANTIALIAS)

        controller.image = ImageTk.PhotoImage(im)
        # notify controller that image has been downloaded
        controller.event_generate("<<ImageLoaded>>")
    except Exception as e:
        print(e)

class MovieFrame(Frame):
    def __init__(self, master=None, main=None):
        Frame.__init__(self,master)
        self.master = master
        self.main = main
        self.bind("<<ImageLoaded>>", self.on_image_loaded)
        self.init_window()



    def init_window(self):
        self.movie_title = StringVar()
        self.movie_title.set("unknown")
        self.fieldname = StringVar()
        self.sort_by = StringVar()
        self.exact_var = BooleanVar()
        self.asc_var = BooleanVar()
        self.pack(fill=BOTH, expand=1)

        self.combobox_fieldname = ttk.Combobox(self, textvariable=self.fieldname)
        self.combobox_fieldname['values'] = ('title', 'overview', 'voteCount', 'voteAverage', 'genre', 'releaseDate')
        self.combobox_fieldname['state'] = 'readonly'
        self.combobox_fieldname.bind('<<ComboboxSelected>>', self.combobox_fieldname_update)

        self.combobox_fieldname.grid(row=0, column=0, padx=10, pady=10)

        self.field_value = Entry(self)
        self.field_value.grid(row=0, column=1, padx=10, pady=10)

        self.check_exact = Checkbutton(self, text='Exact', onvalue=True, offvalue=False, variable=self.exact_var)
        self.check_exact.grid(row=0, column=2, padx=10, pady=10)
        self.check_ascending = Checkbutton(self, text='Ascending', onvalue=True, offvalue=False, variable=self.asc_var)
        self.check_ascending.grid(row=0, column=3, padx=10, pady=10)

        self.combobox_sort_by = ttk.Combobox(self, textvariable=self.sort_by)
        self.combobox_sort_by['values'] = ('title', 'overview', 'voteCount', 'voteAverage', 'genre', 'releaseDate')
        self.combobox_sort_by['state'] = 'readonly'
        self.combobox_sort_by.bind('<<ComboboxSelected>>', self.combobox_sort_by_update)

        self.combobox_sort_by.grid(row=0, column=4, padx=10, pady=10)

        self.search_button = Button(self, text="Search", command=self.search).grid(row=0, column=5, padx=10, pady=10)

        self.imagelab = Label(self, text="Loading image from internet ...")
        self.imagelab.grid(row=1, column=1, sticky=W)

        self.label_title = Label(self, textvariable=self.movie_title).grid(row=1, column=2)

        self.movie_list = Listbox(self)
        self.movie_list.grid(row=1, rowspan=4, column=0, sticky=N+W+S)

        self.movie_list.bind("<<ListboxSelect>>", self.on_movie_select)

        Grid.rowconfigure(self, 3, weight=1)
        Grid.columnconfigure(self, 4, weight=1)

    def search(self):
        params = {
            'field': self.combobox_fieldname.get(),
            'value': self.field_value.get(),
            'exact': self.exact_var.get(),
            'sortBy': self.combobox_sort_by.get(),
            'descending': not self.asc_var.get()
        }
        print(params)
        message = Request('public/get-movies', params)
        self.main.client.send(message)

    def combobox_fieldname_update(self, event):
        self.combobox_fieldname.set(self.fieldname.get())

    def combobox_sort_by_update(self,event):
        self.combobox_sort_by.set(self.sort_by.get())

    def on_image_loaded(self, event):
        self.imagelab.config(image=self.image, width=self.image.width(), height=self.image.height())
    
    def on_movie_select(self, event):
        i = self.movie_list.curselection()[0]
        m = self.movies[i]
        self.movie_title.set(m["title"])
        Thread(target=getImageFromURL, args=(m["posterUrl"], self, f'''movie_image_{m["title"]}_{m["releaseDate"]}.png''')).start()

    def get_movies(self, params):
        message = Request('public/get-movies', params)
        self.main.client.send(message)
        
    def fill_movies(self, movies):

        for filename in glob.glob("movie_image_*"):
            os.remove(filename) 


        self.movies = []
        self.movie_list.delete(0, END)
        for movie in movies:
            self.movies.append(movie)
            self.movie_list.insert(END, movie["title"])

