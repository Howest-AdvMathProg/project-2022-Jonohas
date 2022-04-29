import pandas as pd

from data.models.movie import Movie


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
        df = pd.read_csv("mymoviedb.csv", lineterminator='\n')
        self.movie_list = [(Movie(row["Release_Date"], row["Title"], row["Overview"], row["Popularity"], row["Vote_Count"], row["Vote_Average"], row["Original_Language"], row["Genre"], row["Poster_Url"]).__dict__()) for index, row in df.iterrows()]
        df = None

    # field name, value of the search, is it an exact search true or false, sort by field name, ascending true or fasle
    def search_by_field(self, field, value, exact, sortBy, descending):

 
        search_values = []
        if exact:
            search_values = [movie for movie in self.movie_list if movie[field] == value]
        else:
            search_values = [movie for movie in self.movie_list if value in movie[field]]

        search_values.sort(key=lambda f: f[sortBy], reverse=descending)
        return search_values

    