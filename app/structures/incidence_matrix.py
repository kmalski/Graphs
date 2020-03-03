import numpy

class IncidenceMatrix:
    def __init__(self, file_path):
        self.load_matrix(file_path)

    def load_matrix(self, file_path):
        self.matrix = numpy.loadtxt(file_path, int)

    def __str__(self):
        return str(self.matrix)

    def add_edge(self, vertex_1, vertex_2):
        nr_of_vertexes = len(self.matrix)
        self.matrix = numpy.c_[self.matrix, numpy.zeros(nr_of_vertexes, int)] # adds column with zeros in it

        self.matrix[vertex_1][-1] = 1
        self.matrix[vertex_2][-1] = 1

    def get_neighbors(self, vertex):
        neighbors = numpy.where(self.matrix[vertex] == 1)
        return neighbors[0]
