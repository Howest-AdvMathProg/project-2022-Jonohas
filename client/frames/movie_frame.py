
from sqlite3 import Row
from tkinter import *
from message_handlers.request_message import RequestMessage
from message_handlers.response_message import ResponseMessage
from urllib.request import urlopen
from PIL import Image, ImageTk
import ssl
import base64
from io import BytesIO

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


        im = Image.open(filename).resize((200,160), Image.ANTIALIAS)

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
        self.pack(fill=BOTH, expand=1)

        self.imagelab = Label(self, text="Loading image from internet ...", width=20, height=5)
        self.imagelab.grid(row=0, column=1, sticky=W)

        self.label_title = Label(self, textvariable=self.movie_title).grid(row=0, column=2)

        self.movie_list = Listbox(self)
        self.movie_list.grid(row=0, rowspan=4, column=0, sticky=N+W+S)

        self.movie_list.bind("<<ListboxSelect>>", self.on_movie_select)

        Grid.rowconfigure(self, 3, weight=1)
        Grid.columnconfigure(self, 4, weight=1)

    def on_image_loaded(self, event):
        self.imagelab.config(image=self.image, width=self.image.width(), height=self.image.height())

    
    def on_movie_select(self, event):
        i = self.movie_list.curselection()[0]
        m = self.movies[i]
        self.movie_title.set(m["title"])
        Thread(target=getImageFromURL, args=(m["posterUrl"], self, f'''movie_image_{m["title"]}_{m["releaseDate"]}.png''')).start()

    def get_movies(self, params):
        params['endpoint'] = "/movies"
        message = RequestMessage('GET', params)
        self.main.client.send(message)
        
    def _on_response(self, responseMessage):

        for filename in glob.glob("movie_image_*"):
            os.remove(filename) 

        movies = responseMessage.body["movies"]
        self.movies = []
        self.movie_list.delete(0, END)
        for movie in movies:
            self.movies.append(movie)
            self.movie_list.insert(END, movie["title"])

