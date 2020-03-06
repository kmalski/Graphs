import structures.adjacency_list as adj_list
import structures.adjacency_matrix as adj_matrix

import numpy


class IncidenceMatrix:
    def __init__(self):
        pass

    def from_file(self, file_path: int):
        self.matrix = numpy.loadtxt(file_path, int)

    def init_empty(self, nr_of_vertices: int):
        self.matrix = numpy.empty((nr_of_vertices, 0), int)

    def __str__(self):
        return str(self.matrix)

    def to_string(self):
        return str(self.matrix)

    def add_edge(self, vertex_1: int, vertex_2: int):
        new_column = numpy.zeros(len(self.matrix), int)
        new_column[vertex_1] = 1
        new_column[vertex_2] = 1

        if not any(numpy.array_equal(column, new_column) for column in numpy.transpose(self.matrix)):
            self.matrix = numpy.c_[self.matrix, new_column]

    def get_neighbors(self, vertex: int) -> list:
        neighbors = []
        transposed_matrix = numpy.transpose(self.matrix)

        for i, elem in enumerate(self.matrix[vertex]):
            if elem == 1:
                vertices = numpy.where(transposed_matrix[i] == 1)
                other_vertex = list(filter(lambda x: x != vertex, vertices[0]))
                neighbors.append(*other_vertex)

        return neighbors

    def to_adjacency_matrix(self):
        pass

    def to_adjacency_list(self):
        list = adj_list.AdjacencyList()

        for i in range(len(self.matrix)):
            list.graph[i] = self.get_neighbors(i)

        return list
