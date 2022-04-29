from json import JSONEncoder

class Movie:
    def __init__(self, release_date, title, overview, popularity, vote_count, vote_average, original_language, genre, poster_url):
        self.release_date = release_date
        self.title = title
        self.overview = overview
        self.popularity = popularity
        self.vote_count = vote_count
        self.vote_average = vote_average
        self.original_language = original_language
        self.genre = genre
        self.poster_url = poster_url


    def __dict__(self):
        return { 
            "releaseDate": self.release_date, 
            "title": self.title,
            "overview": self.overview,
            "popularity": self.popularity,
            "voteCount": self.vote_count,
            "voteAverage": self.vote_average,
            "originalLanguage": self.original_language,
            "genre": self.genre,
            "posterUrl": self.poster_url
        }

    def __repr__(self):
        return repr((self.release_date, self.title, self.overview, self.popularity, self.vote_count, self.vote_average, self.original_language, self.genre, self.poster_url))
