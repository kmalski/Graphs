import structures.adjacency_list as adj_list
import structures.incidence_matrix as inc_matrix

import numpy as np


class AdjacencyMatrix:
    def __init__(self):
        pass

    def from_file(self, file_path: str):
        self.matrix = np.loadtxt(file_path, int)

    def to_file(self, file_path: str, add_extension=False):
        if add_extension:
            file_path += '.gam'

        with open(file_path, 'w') as file:
            if self.matrix is not None:
                file.write(self.to_string())

    def from_matrix(self, matrix):
         self.matrix = matrix

    def init_with_zeros(self, nr_of_vertices: int):
        self.matrix = np.zeros((nr_of_vertices, nr_of_vertices), int)

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return str(self.matrix).replace('[', ' ').replace(']', ' ')

    def add_edge(self, vertex_1: int, vertex_2: int):
        self.matrix[vertex_1][vertex_2] = 1
        self.matrix[vertex_2][vertex_1] = 1

    def get_neighbors(self, vertex: int) -> list:
        return [i for i, elem in enumerate(self.matrix[vertex]) if elem == 1]

    def to_incidence_matrix(self):
        matrix = inc_matrix.IncidenceMatrix()
        size = len(self.matrix)
        matrix.init_empty(size)

        for vertex_1 in range(size):
            for vertex_2 in self.get_neighbors(vertex_1):
                matrix.add_edge(vertex_1, vertex_2)

        return matrix

    def to_adjacency_list(self):
        adjacency_list = adj_list.AdjacencyList()

        for vertex in range(len(self.matrix)):
            adjacency_list.set_neighbors(vertex, self.get_neighbors(vertex))

        return adjacency_list
