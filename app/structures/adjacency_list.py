from collections import defaultdict
import structures.adjacency_matrix as gam
import structures.incidence_matrix as gim
import numpy

class AdjacencyList:
    def __init__(self):
        self.graph = defaultdict(list)

    def load_list(self, file_path):
        with open(file_path) as file:
            data_string = file.read()

            for line in iter(data_string.splitlines()):
                line = ''.join(line.split())
                vertex = line[0]
                separator_index = line.index(':')
                neighbors_str = line[separator_index + 1:]
                neighbors = neighbors_str.split(',')
                self.graph[int(vertex)] = map(lambda x: int(x), neighbors)
            
            self.to_incidence_matrix()
        
    def __str__(self):
        result = ''
        for vertex, neighbors in self.graph.items():
            result += vertex + ': '
            result += ', '.join(neighbors)
            result += '\n'
        return result

    def to_string(self):
        return str(self)

    def add_edge(self, vertex_1, vertex_2):
        vertex_1 = str(vertex_1)
        vertex_2 = str(vertex_2)
        self.graph[vertex_1].append(vertex_2)
        self.graph[vertex_2].append(vertex_1)

    def get_neighbors(self, vertex):
        return list(map(lambda x: int(x), self.graph[str(vertex)]))

    def to_adjacency_matrix(self):
        adj_matrix = gam.AdjacencyMatrix()
        nr_of_vertices = max(self.graph.keys()) + 1
        adj_matrix.create_matrix(nr_of_vertices)

        for vertex_1, row in self.graph.items():
            for vertex_2 in row: 
                adj_matrix.add_edge(vertex_1, vertex_2)
                
        return adj_matrix

    def to_incidence_matrix(self):
        pass
        # inc_matrix = gim.IncidenceMatrix()
        # nr_of_vertices = max(self.graph.keys()) + 1
        # inc_matrix.create_matrix(nr_of_vertices)
        
        # for vertex_1, row in self.graph.items():
        #     for vertex_2 in row:
        #         inc_matrix.add_edge(vertex_1, vertex_2)
        
        # return inc_matrix
        