

from MessageHandlers.message import Message
from data.repositories.movie_repository import MovieRepository


class Data(Message):
    def __init__(self, message_queue, io_stream_client, message):
        super().__init__(message_queue, io_stream_client, message)

        movie_repository = MovieRepository()

        self.response_code = 200
        self.body = {
            "movies": movie_repository.movie_list
        }