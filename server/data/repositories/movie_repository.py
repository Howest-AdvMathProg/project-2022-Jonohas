import pandas as pd

from data.models.movie import Movie

class MovieRepository:
    def __init__(self):
        df = pd.read_csv("mymoviedb.csv", lineterminator='\n')
        self.movie_list = [(Movie(row["Release_Date"], row["Title"], row["Overview"], row["Popularity"], row["Vote_Count"], row["Vote_Average"], row["Original_Language"], row["Genre"], row["Poster_Url"]).__dict__()) for index, row in df.iterrows()]
        df = None
