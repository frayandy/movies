from unittest import TestCase


class FakeResponse:

    def __init__(self, data=None, status_code=None):
        self._data = data
        self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code

    def json(self):
        return self._data


class BaseTestCase(TestCase):
    pass
