import structures.adjacency_list as adj_list
import structures.incidence_matrix as inc_matrix

import numpy as np
import sys


class AdjacencyMatrix:
    def __init__(self, matrix):
        self.matrix = matrix

    @classmethod
    def from_file(cls, file_path: str):
        return cls(np.loadtxt(file_path, int))

    @classmethod
    def from_matrix(cls, matrix):
        return cls(matrix)

    @classmethod
    def init_with_zeros(cls, nr_of_vertices: int):
        return cls(np.zeros((nr_of_vertices, nr_of_vertices), int))

    def to_file(self, file_path: str, add_extension=False):
        if add_extension:
            file_path += '.gam'

        with open(file_path, 'w') as file, np.printoptions(threshold=sys.maxsize, linewidth=np.inf):
            if self.matrix is not None:
                file.write(self.to_string())

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return str(self.matrix).replace('[', ' ').replace(']', ' ')

    def add_edge(self, vertex_1: int, vertex_2: int):
        self.matrix[vertex_1][vertex_2] = 1
        self.matrix[vertex_2][vertex_1] = 1

    def get_neighbors(self, vertex: int) -> list:
        return [i for i, elem in enumerate(self.matrix[vertex]) if elem == 1]

    def get_number_of_edges(self) ->int:
        return sum(sum(self.matrix)) // 2

    def to_incidence_matrix(self):
        size = len(self.matrix)
        matrix = inc_matrix.IncidenceMatrix.init_empty(size)

        for vertex_1 in range(size):
            for vertex_2 in self.get_neighbors(vertex_1):
                matrix.add_edge(vertex_1, vertex_2)

        return matrix

    def to_adjacency_list(self):
        adjacency_list = adj_list.AdjacencyList.init_empty()

        for vertex in range(len(self.matrix)):
            adjacency_list.set_neighbors(vertex, self.get_neighbors(vertex))

        return adjacency_list


    def to_adjacency_list_with_weights(self, weights):
        adjacency_list = adj_list.AdjacencyListWithWeights.init_empty()

        weight_number = 0
        for vertex in range(len(self.matrix)):
            adjacency_list.graph[vertex] #creating isolated nodes
            if any(self.matrix[vertex]):
                neighbours = self.get_neighbors(vertex)
                for neighbour in neighbours:
                    if weight_number >= len(weights):
                        break
                    weight_number += adjacency_list.add_edge(vertex, neighbour, weights[weight_number])

        return adjacency_list

