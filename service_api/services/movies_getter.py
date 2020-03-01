from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
from http import HTTPStatus

import requests
from werkzeug.exceptions import InternalServerError

from service_api.constants import (
    PEOPLE_GHIBLI_URI, MOVIES_GHIBLI_URI, PEOPLE_KEY, FILMS_KEY, MOVIES_PEOPLE_WORKERS_COUNT
)
from service_api.services import BaseGetter


class MoviesPeopleGetter(BaseGetter):

    @classmethod
    def get_movies_and_characters(cls):
        with ThreadPoolExecutor(max_workers=MOVIES_PEOPLE_WORKERS_COUNT) as executor:
            key_func_map = {PEOPLE_KEY: cls._get_people, FILMS_KEY: cls._get_movies}
            responses = {}
            futures_map = {executor.submit(func): k for k, func in key_func_map.items()}
            for future in as_completed(futures_map):
                responses[futures_map[future]] = future.result()

        return responses

    @classmethod
    def get_movies_with_characters(cls):
        movies_and_characters = cls.get_movies_and_characters()
        movies = movies_and_characters[FILMS_KEY]
        for character in movies_and_characters[PEOPLE_KEY]:
            for character_film in character[FILMS_KEY]:
                *_, film_id = character_film.split('/')

                if film_id in movies:
                    movies[film_id][PEOPLE_KEY].append(character)

        return [movie for k, movie in movies.items()]

    @staticmethod
    def _get_people():
        response = requests.get(PEOPLE_GHIBLI_URI)
        if response.status_code != HTTPStatus.OK:
            raise InternalServerError('Something went wrong')
        return response.json()

    @staticmethod
    def _get_movies():
        response = requests.get(MOVIES_GHIBLI_URI)
        if response.status_code != HTTPStatus.OK:
            raise InternalServerError('Something went wrong')

        movies_map = {}
        for movie in response.json():
            movie[PEOPLE_KEY] = []
            movies_map[movie['id']] = movie

        return movies_map
