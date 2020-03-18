from copy import deepcopy

def is_graphic_sequence(sequence_par: list):
    sequence = deepcopy(sequence_par)
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
