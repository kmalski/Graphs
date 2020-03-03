import numpy

class AdjacencyMatrix:
    def __init__(self, file_path):
        self.load_matrix(file_path)

    def load_matrix(self, file_path):
        self.matrix = numpy.loadtxt(file_path, int)

    def __str__(self):
        return str(self.matrix)

    def add_edge(self, vertex_1, vertex_2):
        self.matrix[vertex_1][vertex_2] = 1
        self.matrix[vertex_2][vertex_1] = 1

    def get_neighbors(self, vertex):
        return [i for i, elem in enumerate(self.matrix[vertex]) if elem == 1]