import structures.adjacency_list as gal
import structures.incidence_matrix as gim
import numpy

class AdjacencyMatrix:
    def __init__(self):
        pass

    def load_matrix(self, file_path):
        self.matrix = numpy.loadtxt(file_path, int)

    def create_matrix(self, nr_of_vertices):
        self.matrix = numpy.zeros((nr_of_vertices, nr_of_vertices), int)

    def __str__(self):
        return str(self.matrix)

    def to_string(self):
        return str(self.matrix)

    def add_edge(self, vertex_1, vertex_2):
        self.matrix[vertex_1][vertex_2] = 1
        self.matrix[vertex_2][vertex_1] = 1

    def get_neighbors(self, vertex):
        return [i for i, elem in enumerate(self.matrix[vertex]) if elem == 1]

    def to_incidence_matrix(self):
        pass

    def to_adjacency_list(self):
        pass