from structures.adjacency_list import AdjacencyList

import random
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

def randomize(graph, max_it):
    if not isinstance(graph, AdjacencyList):
        graph = graph.to_adjacency_list()

    if graph.get_amount_of_edges() < 2 or graph.get_amount_of_vertices() < 4:
        return False

    for _ in range(max_it):
        random_result = graph.get_two_random_separated_edges()
        if random_result is not None:
            edge_1, edge_2 = random_result
            a, b = edge_1
            c, d = edge_2

            if not graph.is_edge(a, d) and not graph.is_edge(b, c):
                graph.remove_edge(a, b)
                graph.remove_edge(c, d)
                graph.add_edge(a, d)
                graph.add_edge(b, c) 
                return True
            elif not graph.is_edge(a, c) and not graph.is_edge(b, d):
                graph.remove_edge(a, b)
                graph.remove_edge(c, d)
                graph.add_edge(a, c)
                graph.add_edge(b, d)
                return True

    return False