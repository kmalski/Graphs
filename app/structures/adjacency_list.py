from collections import defaultdict


class AdjacencyList:
    def __init__(self):
        self.graph = defaultdict(list)

    def from_string(self, data_string):
        for line in iter(data_string.splitlines()):
            line = ''.join(line.split())
            vertex = line[0]
            seprator_index = line.index(':')
            neighbors_str = line[seprator_index + 1:]
            neighbors = neighbors_str.split(',')
            self.graph[vertex] = neighbors
        
    def to_string(self):
        result = ''
        for vertex, neighbors in self.graph.items():
            result += vertex + ': '
            result += ', '.join(neighbors)
            result += '\n'
        return result

    def add_edge(self, vertex_1, vertex_2):
        vertex_1 = str(vertex_1)
        vertex_2 = str(vertex_2)
        self.graph[vertex_1].append(vertex_2)
        self.graph[vertex_2].append(vertex_1)

    def get_neighbors(self, vertex):
        return list(map(lambda x: int(x), self.graph[str(vertex)]))