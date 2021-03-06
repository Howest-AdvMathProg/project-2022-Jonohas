import pandas as pd

from data.models.movie import Movie
import seaborn as sns
import matplotlib.pyplot as plt
import base64

from multiprocessing import Process, Pipe


def sort_title(value):
    return value["title"]

def sort_release_date(value):
    return value["release_date"]


def sort_popularity(value):
    return value["popularity"]


def sort_vote_count(value):
    return value["vote_count"]


def sort_vote_average(value):
    return value["vote_average"]


def sort_original_language(value):
    return value["original_language"]

class MovieRepository:
    def __init__(self):
        self.df = pd.read_csv("mymoviedb.csv", lineterminator='\n')
        self.movie_list = [(Movie(row["Release_Date"], row["Title"], row["Overview"], row["Popularity"], row["Vote_Count"], row["Vote_Average"], row["Original_Language"], row["Genre"], row["Poster_Url"]).__dict__()) for index, row in self.df.iterrows()]

        self.graph = ""

    # field name, value of the search, is it an exact search true or false, sort by field name, ascending true or fasle
    def search_by_field(self, field, value, exact, sortBy, descending):

 
        search_values = []
        if exact:
            search_values = [movie for movie in self.movie_list if movie[field] == value]
        else:
            search_values = [movie for movie in self.movie_list if value in movie[field]]

        search_values.sort(key=lambda f: f[sortBy], reverse=descending)
        return search_values

    def create_frequency_graph(self):
        parent_conn, child_conn = Pipe()
        p = Process(target=self.get_graph, args=(child_conn,))
        p.start()

        self.graph = parent_conn.recv()
        p.join()

        return self.graph
        


    def get_graph(self, conn):
        graph = sns.histplot(data = self.df, x='Release_Date', stat='count')
        plt.savefig('frequency_graph.png')
        self.graph = open("frequency_graph.png","rb").read()
        conn.send(self.graph)
        

    