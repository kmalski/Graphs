from typing import Union


def is_graphic_sequence(sequence: Union[list, str]):
    if isinstance(sequence, str):
        sequence = list(map(lambda x: int(x), sequence.split()))

    size = len(sequence)
    sequence.sort(reverse=True)

    while True:
        if not any(sequence):
            return True
        if sequence[0] < 0 or sequence[0] >= size or any(i < 0 for i in sequence):
            return False

        for i in range(sequence[0] + 1):
            sequence[i] -= 1

        sequence[0] = 0
        sequence.sort(reverse=True)


class GraphicSequence:
    def __init__(self, sequence):
        self.sequence = sequence

    @classmethod
    def from_string(cls, string: str):
        sequence = list(map(lambda x: int(x), string.split()))

        if is_graphic_sequence(sequence):
            return cls(sequence)
        else:
            raise AttributeError
