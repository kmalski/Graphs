import structures.adjacency_list as adj_list
import structures.incidence_matrix as inc_matrix

import numpy


class AdjacencyMatrix:
    def __init__(self):
        pass

    def from_file(self, file_path: str):
        self.matrix = numpy.loadtxt(file_path, int)

    def init_with_zeros(self, nr_of_vertices: int):
        self.matrix = numpy.zeros((nr_of_vertices, nr_of_vertices), int)

    def __str__(self):
        return str(self.matrix)

    def to_string(self):
        return str(self.matrix)

    def add_edge(self, vertex_1: int, vertex_2: int):
        self.matrix[vertex_1][vertex_2] = 1
        self.matrix[vertex_2][vertex_1] = 1

    def get_neighbors(self, vertex: int) -> list:
        return [i for i, elem in enumerate(self.matrix[vertex]) if elem == 1]

    def to_incidence_matrix(self):
        pass

    def to_adjacency_list(self):
        list = adj_list.AdjacencyList()
        for i in range(len(self.matrix)):
            list.graph[i] = self.get_neighbors(i)
        return list
