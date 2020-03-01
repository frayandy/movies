from http import HTTPStatus
from unittest.mock import patch

from werkzeug.exceptions import InternalServerError

from service_api.services.movies_getter import MoviesPeopleGetter
from tests import BaseTestCase, FakeResponse

MOVIES_WITH_PEOPLE_DATA = [
    {
        'id': '1',
        'title': 'Star Wars Episode I: The Phantom Menace',
        'description': 'A long time ago in a galaxy far, far away...',
        'director': 'George Lukas',
        'producer': 'George Lukas',
        'release_date': '2004',
        'rt_score': '99',
        'people': [
            {
                'id': '1',
                'name': 'John Smith',
                'gender': 'man',
                'age': '20',
                'films': ['https://bbc.com/1']
            }
        ]
    },
    {
        'id': '2',
        'title': 'Star Wars Episode II: Attack of the Clones',
        'description': 'A long time ago in a galaxy far, far away...',
        'director': 'George Lukas',
        'producer': 'George Lukas',
        'release_date': '2004',
        'rt_score': '99',
        'people': [
            {
                'id': '2',
                'name': 'Luke Skywalker',
                'gender': 'man',
                'age': '30',
                'films': ['https://bbc.com/2']
            },
            {
                'id': '3',
                'name': 'Darth Vader',
                'gender': 'man',
                'age': '40',
                'films': ['https://bbc.com/2', 'https://bbc.com/3']
            }
        ]
     },
    {
        'id': '3',
        'title': 'Star Wars Episode III: Revenge of the Sith',
        'description': 'A long time ago in a galaxy far, far away...',
        'director': 'George Lukas',
        'producer': 'George Lukas',
        'release_date': '2004',
        'rt_score': '99',
        'people': [
            {
                'id': '3',
                'name': 'Darth Vader',
                'gender': 'man',
                'age': '40',
                'films': ['https://bbc.com/2', 'https://bbc.com/3']
            }
        ]
    }
]

PEOPLE_DATA = [
    {
        'id': '1',
        'name': 'John Smith',
        'gender': 'man',
        'age': '20',
        'films': ['https://bbc.com/1']
    },
    {
        'id': '2',
        'name': 'Luke Skywalker',
        'gender': 'man',
        'age': '30',
        'films': ['https://bbc.com/2']
    },
    {
        'id': '3',
        'name': 'Darth Vader',
        'gender': 'man',
        'age': '40',
        'films': ['https://bbc.com/2', 'https://bbc.com/3']
    }
]

MOVIES_DATA = [
    {
        'id': '1',
        'title': 'Star Wars Episode I: The Phantom Menace',
        'description': 'A long time ago in a galaxy far, far away...',
        'director': 'George Lukas',
        'producer': 'George Lukas',
        'release_date': '2004',
        'rt_score': '99',
        'people': []
    },
    {
        'id': '2',
        'title': 'Star Wars Episode II: Attack of the Clones',
        'description': 'A long time ago in a galaxy far, far away...',
        'director': 'George Lukas',
        'producer': 'George Lukas',
        'release_date': '2004',
        'rt_score': '99',
        'people': []
    },
    {
        'id': '3',
        'title': 'Star Wars Episode III: Revenge of the Sith',
        'description': 'A long time ago in a galaxy far, far away...',
        'director': 'George Lukas',
        'producer': 'George Lukas',
        'release_date': '2004',
        'rt_score': '99',
        'people': []
    }
]


class TestGetters(BaseTestCase):

    @patch('service_api.services.movies_getter.requests.get')
    def test_get_people(self, request):
        request.return_value = FakeResponse(PEOPLE_DATA, HTTPStatus.OK)
        result = MoviesPeopleGetter._get_people()
        self.assertEqual(result, PEOPLE_DATA)

    @patch('service_api.services.movies_getter.requests.get')
    def test_get_people_empty_list(self, request):
        mock_data = []
        request.return_value = FakeResponse(mock_data, HTTPStatus.OK)
        result = MoviesPeopleGetter._get_people()
        self.assertEqual(result, mock_data)

    @patch('service_api.services.movies_getter.requests.get')
    def test_get_people_bad_request(self, request):
        request.return_value = FakeResponse(None, HTTPStatus.BAD_REQUEST)
        with self.assertRaises(InternalServerError, msg='Something went wrong') as e:
            MoviesPeopleGetter._get_people()

    @patch('service_api.services.movies_getter.requests.get')
    def test_get_movies(self, request):
        request.return_value = FakeResponse(MOVIES_DATA, HTTPStatus.OK)
        result = MoviesPeopleGetter._get_movies()
        self.assertEqual(result, {m['id']: m for m in MOVIES_DATA})

    @patch('service_api.services.movies_getter.requests.get')
    def test_get_movies_bad_request(self, request):
        request.return_value = FakeResponse(None, HTTPStatus.BAD_REQUEST)
        with self.assertRaises(InternalServerError, msg='Something went wrong') as e:
            MoviesPeopleGetter._get_movies()

    @patch('service_api.services.movies_getter.requests.get')
    def test_get_movies_empty_list(self, request):
        mock_data = []
        request.return_value = FakeResponse(mock_data, HTTPStatus.OK)
        result = MoviesPeopleGetter._get_movies()
        self.assertEqual(result, {})

    @patch('service_api.services.movies_getter.MoviesPeopleGetter._get_people')
    @patch('service_api.services.movies_getter.MoviesPeopleGetter._get_movies')
    def test_get_movies_with_peoples(self, movies, people):
        movies.return_value = {m['id']: m for m in MOVIES_DATA}
        people.return_value = PEOPLE_DATA
        response = MoviesPeopleGetter.get_movies_with_characters()
        self.assertEqual(response, MOVIES_WITH_PEOPLE_DATA)

    @patch('service_api.services.movies_getter.MoviesPeopleGetter._get_people')
    @patch('service_api.services.movies_getter.MoviesPeopleGetter._get_movies')
    def test_get_movies_with_peoples_no_movies(self, movies, people):
        movies.return_value = {}
        people.return_value = PEOPLE_DATA
        response = MoviesPeopleGetter.get_movies_with_characters()
        self.assertEqual(response, [])

    @patch('service_api.services.movies_getter.MoviesPeopleGetter._get_people')
    @patch('service_api.services.movies_getter.MoviesPeopleGetter._get_movies')
    def test_get_movies_with_peoples_no_people(self, movies, people):
        movies.return_value = {m['id']: m for m in MOVIES_DATA}
        people.return_value = []
        response = MoviesPeopleGetter.get_movies_with_characters()
        self.assertEqual(response, MOVIES_DATA)
