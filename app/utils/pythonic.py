from itertools import groupby
from dataclasses import dataclass


def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


@dataclass(eq=True, order=True)
class MutableInt:
    value: int = 0

    def __iadd__(self, other: int):
        self.value += other
        return self

    def __isub__(self, other: int):
        self.value += other
        return self

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
