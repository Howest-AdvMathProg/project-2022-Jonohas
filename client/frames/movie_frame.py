
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


        im = Image.open(filename).resize((300,450), Image.ANTIALIAS)

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

        self.filter_frame = Frame(self)

        self.combobox_fieldname = ttk.Combobox(self.filter_frame, textvariable=self.fieldname)
        self.combobox_fieldname['values'] = ('title', 'overview', 'voteCount', 'voteAverage', 'genre', 'releaseDate')
        self.combobox_fieldname['state'] = 'readonly'
        self.combobox_fieldname.bind('<<ComboboxSelected>>', self.combobox_fieldname_update)

        self.combobox_fieldname.grid(row=0, column=0, padx=10, pady=10)

        self.field_value = Entry(self.filter_frame)
        self.field_value.grid(row=0, column=1, padx=10, pady=10)

        self.check_exact = Checkbutton(self.filter_frame, text='Exact', onvalue=True, offvalue=False, variable=self.exact_var)
        self.check_exact.grid(row=0, column=2, padx=10, pady=10)
        self.check_ascending = Checkbutton(self.filter_frame, text='Ascending', onvalue=True, offvalue=False, variable=self.asc_var)
        self.check_ascending.grid(row=0, column=3, padx=10, pady=10)

        self.combobox_sort_by = ttk.Combobox(self.filter_frame, textvariable=self.sort_by)
        self.combobox_sort_by['values'] = ('title', 'overview', 'voteCount', 'voteAverage', 'genre', 'releaseDate')
        self.combobox_sort_by['state'] = 'readonly'
        self.combobox_sort_by.bind('<<ComboboxSelected>>', self.combobox_sort_by_update)

        self.combobox_sort_by.grid(row=0, column=4, padx=10, pady=10)

        self.search_button = Button(self.filter_frame, text="Search", command=self.search).grid(row=0, column=5, padx=10, pady=10)
        self.filter_frame.grid(row=0,column=0, columnspan=4, sticky=N+S+E+W)

        self.imagelab = Label(self, text="Loading image from internet ...")
        self.imagelab.grid(row=1, rowspan=4, column=3, sticky=W)


        self.movie_title = StringVar()
        self.movie_title.set("unknown")
        self.label_title = Label(self, textvariable=self.movie_title, anchor=W).grid(row=1,columnspan=8, column=4, sticky='w')

        self.movie_overview = StringVar()
        self.movie_overview.set('unknown')
        self.label_overview = Message( self, textvariable=self.movie_overview, anchor=W).grid(row=2, columnspan=8 , column=4, sticky='we')

        self.row_mini_stats = Frame(self)

        self.movie_popularity = StringVar()
        self.movie_popularity.set('unknown')
        Label(self.row_mini_stats, text="Vote popularity:").grid(row=0, column=0)
        self.label_popularity = Label(self.row_mini_stats, textvariable=self.movie_popularity).grid(row=0, column=1)
    
        self.movie_vote_count = StringVar()
        self.movie_vote_count.set('unknown')
        Label(self.row_mini_stats, text="Vote count:").grid(row=0, column=2)
        self.label_vote_count = Label(self.row_mini_stats, textvariable=self.movie_vote_count).grid(row=0, column=3)

        self.movie_vote_avg = StringVar()
        self.movie_vote_avg.set('unknown')
        Label(self.row_mini_stats, text="Vote average:").grid(row=0, column=4)
        self.label_vote_avg = Label(self.row_mini_stats, textvariable=self.movie_vote_avg).grid(row=0, column=5)

        self.row_mini_stats.grid(row=3, column=4, columnspan=8, sticky=W)
        


        self.movie_list = Listbox(self)
        self.movie_list.grid(row=1, rowspan=7, column=0, columnspan=3, sticky=N+W+S+E)

        self.movie_list.bind("<<ListboxSelect>>", self.on_movie_select)

        Grid.rowconfigure(self, 7, weight=1)
        Grid.columnconfigure(self, 10, weight=1)

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
        self.movie_overview.set(m['overview'])
        self.movie_vote_avg.set(m['voteAverage'])
        self.movie_vote_count.set(m['voteCount'])
        self.movie_popularity.set(m['popularity'])

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

