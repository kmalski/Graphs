import structures.adjacency_list as adj_list
import structures.adjacency_matrix as adj_matrix

import numpy as np
import sys

class IncidenceMatrix:
    def __init__(self, matrix):
        self.matrix = matrix

    @classmethod
    def from_file(cls, file_path: int):
        return cls(np.loadtxt(file_path, int))

    @classmethod
    def init_empty(cls, nr_of_vertices: int):
        return cls(np.empty((nr_of_vertices, 0), int))

    def to_file(self, file_path: str, add_extension=False):
        if add_extension:
            file_path += '.gim'

        with open(file_path, 'w') as file, np.printoptions(threshold=sys.maxsize, linewidth=np.inf):
            if self.matrix is not None:
                file.write(self.to_string())

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return str(self.matrix).replace('[', ' ').replace(']', ' ')

    def add_edge(self, vertex_1: int, vertex_2: int):
        new_column = np.zeros(len(self.matrix), int)
        new_column[vertex_1] = 1
        new_column[vertex_2] = 1

        if not any(np.array_equal(column, new_column) for column in np.transpose(self.matrix)):
            self.matrix = np.c_[self.matrix, new_column]

    def get_neighbors(self, vertex: int) -> list:
        neighbors = []
        transposed_matrix = np.transpose(self.matrix)

        for i, elem in enumerate(self.matrix[vertex]):
            if elem == 1:
                vertices = np.where(transposed_matrix[i] == 1)
                other_vertex = list(filter(lambda x: x != vertex, vertices[0]))
                neighbors.append(*other_vertex)

        return neighbors

    def to_adjacency_matrix(self):
        size = len(self.matrix)
        matrix = adj_matrix.AdjacencyMatrix.init_with_zeros(size)

        for vertex_1 in range(size):
            for vertex_2 in self.get_neighbors(vertex_1):
                matrix.add_edge(vertex_1, vertex_2)

        return matrix

    def to_adjacency_list(self):
        adjacency_list = adj_list.AdjacencyList.init_empty()

        for vertex in range(len(self.matrix)):
            adjacency_list.set_neighbors(vertex, self.get_neighbors(vertex))

        return adjacency_list
