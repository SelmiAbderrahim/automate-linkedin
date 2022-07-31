import time
from random import uniform


class Base:
    def __init__(self):
        self._url: str = "https://www.linkedin.com/feed"
        self._short_sleep_range: tuple = (0.5, 0.9)
        self._long_sleep_range: tuple = (1.5, 4.9)

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, link: str) -> None:
        self._url = link

    @property
    def short_sleep_range(self) -> tuple:
        return self._short_sleep_range

    @short_sleep_range.setter
    def short_sleep_range(self, range: tuple) -> None:
        self._short_sleep_range = range

    @property
    def long_sleep_range(self) -> tuple:
        return self._long_sleep_range

    @long_sleep_range.setter
    def long_sleep_range(self, range: tuple) -> None:
        self._long_sleep_range = range

    def short_nap(self):
        a, b = self._short_sleep_range
        time.sleep(uniform(a, b))

    def long_nap(self):
        a, b = self._long_sleep_range
        time.sleep(uniform(a, b))
