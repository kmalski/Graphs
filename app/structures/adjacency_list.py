import structures.adjacency_matrix as adj_matrix
import structures.incidence_matrix as inc_matrix

import numpy
from collections import defaultdict


class AdjacencyList:
    def __init__(self):
        self.graph = defaultdict(list)

    def from_file(self, file_path: str):
        with open(file_path) as file:
            data_string = file.read()

            for line in iter(data_string.splitlines()):
                line = ''.join(line.split())
                vertex = line[0]
                separator_index = line.index(':')
                neighbors_str = line[separator_index + 1:]
                neighbors = neighbors_str.split(',')
                self.graph[int(vertex)] = list(map(lambda x: int(x), neighbors))

    def __str__(self):
        result = ''
        for vertex, neighbors in self.graph.items():
            result += str(vertex) + ': '
            result += ', '.join(map(str, neighbors))
            result += '\n'
        return result

    def to_string(self):
        return str(self)

    def add_edge(self, vertex_1: int, vertex_2: int):
        self.graph[vertex_1].append(vertex_2)
        self.graph[vertex_2].append(vertex_1)

    def get_neighbors(self, vertex: int) -> list:
        return self.graph[vertex]

    def to_adjacency_matrix(self):
        matrix = adj_matrix.AdjacencyMatrix()
        matrix.init_with_zeros(len(self.graph))

        for vertex_1, row in self.graph.items():
            for vertex_2 in row:
                matrix.add_edge(vertex_1, vertex_2)

        return matrix

    def to_incidence_matrix(self):
        matrix = inc_matrix.IncidenceMatrix()
        matrix.init_empty(len(self.graph))

        for vertex_1, row in self.graph.items():
            for vertex_2 in row:
                matrix.add_edge(vertex_1, vertex_2)

        return matrix
