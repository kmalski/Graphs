import structures.adjacency_matrix as adj_matrix
import structures.incidence_matrix as inc_matrix

from collections import defaultdict


class AdjacencyList:
    def __init__(self, graph):
        self.graph = graph

    @classmethod
    def from_file(cls, file_path: str):
        graph = defaultdict(list)

        with open(file_path) as file:
            data_string = file.read()

            for line in iter(data_string.splitlines()):
                line = ''.join(line.split())
                vertex = line[0]
                separator_index = line.index(':')
                neighbors_str = line[separator_index + 1:]
                neighbors = neighbors_str.split(',')
                graph[int(vertex)] = list(map(lambda x: int(x), neighbors))

        return cls(graph)

    @classmethod
    def init_empty(cls):
        return cls(defaultdict(list))

    @classmethod
    def from_graphic_sequence(cls, sequence : list):
        graph = defaultdict(list)
        sequence.sort(reverse=True)

        for i in range(len(sequence)):
            edges = sequence[i] - len(graph[i])

            for j in range (i + 1, len(sequence)):
                if edges == 0:
                    break

                if i == j or j in graph[i]:
                    continue

                if len(graph[j]) < sequence[j]:
                    graph[j].append(i)
                    graph[i].append(j)
                    edges -= 1
            
        return cls(graph)

    def to_file(self, file_path: str, add_extension=False):
        if add_extension:
            file_path += '.gal'

        with open(file_path, 'w') as file:
            if self.graph is not None:
                file.write(self.to_string())

    def __str__(self):
        result = ''
        for vertex, neighbors in self.graph.items():
            result += str(vertex) + ': '
            result += ', '.join(map(str, neighbors))
            result += '\n'
        return result

    def to_string(self):
        return str(self)

    def set_neighbors(self, vertex: int, neighbors: list):
        self.graph[vertex] = neighbors

    def add_edge(self, vertex_1: int, vertex_2: int):
        self.graph[vertex_1].append(vertex_2)
        self.graph[vertex_2].append(vertex_1)

    def get_neighbors(self, vertex: int) -> list:
        return self.graph[vertex]

    def to_adjacency_matrix(self):
        matrix = adj_matrix.AdjacencyMatrix.init_with_zeros(len(self.graph))

        for vertex_1, row in self.graph.items():
            for vertex_2 in row:
                matrix.add_edge(vertex_1, vertex_2)

        return matrix

    def to_incidence_matrix(self):
        matrix = inc_matrix.IncidenceMatrix.init_empty(len(self.graph))

        for vertex_1, row in self.graph.items():
            for vertex_2 in row:
                matrix.add_edge(vertex_1, vertex_2)

        return matrix
