from structures.adjacency_list import AdjacencyList

class AdjacencyListWithWeights(AdjacencyList):
    def __init__(self, graph):
        self.graph = graph