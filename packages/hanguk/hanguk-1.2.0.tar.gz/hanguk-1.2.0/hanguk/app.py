import json
import os

from collections.abc import Generator, Iterable, Iterator
from io import StringIO
from itertools import islice
from typing import Any, List, Tuple


class Hanguk:
    """
    The official Korean language romanization system in Python.

    The class has the following methods:

    __init__(self, text: str)
    - constructor method of the class which initializes the text property.

    read(self) -> str
    - This method returns a string read by stream() method.

    stream(self) -> StringIO
    - This method returns as a StringIO object.

    _data(self)
    - A private method that reads data.json file located in static folder relative to the current file.

    _jamo(self, char: str) -> Tuple[str]
    - A private method which takes a character as an input and returns a tuple with its corresponding Jamo characters (used in Korean language) by performing some mathematical calculations.
    - If an input character is not Korean character then it returns an empty string and the input character.

    _unpack(self, text: str) -> Generator[Tuple[str]]
    - This method takes a text string as an input, converts it into individual Korean characters, and converts them to jamo using _jamo() method.
    - Returns a generator object of tuple strings containing jamo characters of characters in input text string.

    _chunks(iterable: Iterable[Any], size: int) -> Iterator[List[str]]
    - This is a private static method which takes an iterable and a size parameter and returns an iterator object that chunks the input iterable into same-sized chunks defined by the size parameter.
    """

    def __init__(self, text: str):
        self.text = text

    @property
    def _data(self):
        with open(os.path.join(os.path.dirname(__file__), 'static', 'data.json'), 'r', encoding='utf-8') as f:
            return json.load(f)

    def _jamo(self, char: str) -> Tuple[str]:
        if 44032 <= (x := ord(char)) <= 55203:
            a = x - 44032
            b = a % 28
            c = 1 + ((a - b) % 588) // 28
            d = 1 + a // 588
            q = [*map(sum, zip(*[[d, c, b], [4351, 4448, 4519]]))]
            if b:
                return (chr(q[0]), chr(q[1]), chr(q[2]))
            return (chr(q[0]), chr(q[1]), '')
        return ('', char, '')

    def _unpack(self, text: str) -> Generator[Tuple[str]]:
        for i in range(len(text)):
            if i not in [0, len(text) - 1]:
                yield self._jamo(text[i])
            else:
                if i == 0:
                    yield ('', *self._jamo(text[i]))
                else:
                    yield (*self._jamo(text[i]), '', '')

    def read(self) -> str:
        return self.stream().read()

    def stream(self) -> StringIO:
        if len(self.text) == 1:
            return StringIO(self.text)

        output = StringIO()

        for chunk in self._chunks((j for i in self._unpack(self.text) for j in i), 3):
            try:
                output.write(self._data[f"{chunk[0] or '-'}{chunk[1] or '-'}"])
            except KeyError:
                pass
            try:
                output.write(self._data[f"-{chunk[2]}"])
            except KeyError:
                output.write(chunk[2])

        output.seek(0)
        return output

    @staticmethod
    def _chunks(iterable: Iterable[Any], size: int) -> Iterator[List[str]]:
        def slice_size(g): return lambda: tuple(islice(g, size))
        return iter(slice_size(iter(iterable)), ())
