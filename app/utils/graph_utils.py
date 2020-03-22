from structures.adjacency_list import AdjacencyList
from structures.adjacency_matrix import AdjacencyMatrix

import numpy as np
import random
from copy import deepcopy
from typing import List, Tuple
from collections import defaultdict


def is_graphic_sequence(sequence_par: List[int]):
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


def randomize(graph, max_it: int = 100):
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

def gen_randgraph_NL(N: int, L: int) -> AdjacencyMatrix:
    matrix = np.zeros((N, N), int)
    tmp = 0
    while tmp < L:
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        if x != y and matrix[x][y] != 1:
            matrix[x][y] = 1
            matrix[y][x] = 1
            tmp += 1

    return AdjacencyMatrix.from_matrix(matrix)

def gen_randgraph_NP(N: int, P: float) -> AdjacencyMatrix:
    matrix = np.zeros((N, N), int)
    for i in range(N):
        for j in range(i):
            if random.random() < P:
                matrix[i][j] = 1
                matrix[j][i] = 1
    
    return AdjacencyMatrix.from_matrix(matrix)

def randomize_times(graph, n: int, max_it=100):
    for _ in range(n):
        randomize(graph, max_it)


def find_biggest_components(components: List[int]) -> Tuple[List[int]]:
    sizes = defaultdict(int)
    for component_name in components:
        sizes[component_name] += 1

    biggest_comp_size = max(sizes.values())
    biggest_components_names = [comp for comp, size in sizes.items() if size == biggest_comp_size]

    biggest_components = []
    for component_name in biggest_components_names:
        biggest_components.append([vertex for vertex, component in enumerate(components)
                                   if component == component_name])

    return tuple(biggest_components)


def generate_random_euler_graph(verticles_amount: int) -> AdjacencyList:
    while True:
        sequence = 2 * [random.randrange(2, verticles_amount, 2) for _ in range(verticles_amount // 2)]

        if len(sequence) == verticles_amount - 1:
            sequence.append(random.randrange(2, verticles_amount, 2))

        if is_graphic_sequence(sequence):
            return AdjacencyList.from_graphic_sequence(sequence)
