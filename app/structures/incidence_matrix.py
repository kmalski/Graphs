class IncidenceMatrix:
    def __init__(self):
        self.graph = []
        self.size = 0

    def from_string(self, data_string):
        for line in iter(data_string.splitlines()):
            line = ''.join(line.split())
            self.graph.append(line.split('|'))
        
        self.size = len(self.graph[0])

    def to_string(self):
        result = ''
        for row in self.graph:
            result += str(row) + '\n'
        return result

    def add_edge(self, vertex_1, vertex_2):
        def col_appender(row):
            row.append('0')
            return row

        self.graph = list(map(col_appender, self.graph))

        self.graph[vertex_1][self.size] = '1'
        self.graph[vertex_2][self.size] = '1'

    def get_neighbors(self, vertex):
        neighbors = []
        transposed_graph = tuple(zip(*self.graph))
        for col, elem in enumerate(self.graph[vertex]):
            if elem == '1':
                neighbor = transposed_graph[col].index('1')
                neighbors.append(neighbor if neighbor != vertex else transposed_graph[col].index('1', vertex + 1))

        return neighbors
