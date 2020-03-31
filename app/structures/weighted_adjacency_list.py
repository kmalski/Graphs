from utils.pythonic import all_equal

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Dict
import numpy as np


@dataclass(eq=True, order=True)
class Node:
    index: int
    weight: int


class WeightedAdjacencyList:
    def __init__(self, graph):
        self.graph = graph

    @classmethod
    def init_empty(cls):
        return cls(defaultdict(list))

    def __str__(self):
        result = ''
        for vertex, neighbors in self.graph.items():
            result += str(vertex) + ': '
            result += ', '.join(map(str, neighbors))
            result += '\n'
        return result

    def add_edge(self, first: int, second: int, weight: int) -> bool:
        if not any(neigbour.index == second for neigbour in self.graph[first]):
            self.graph[first].append(Node(second, weight))
            self.graph[second].append(Node(first, weight))
            return True
        return False

    def has_vertex(self, vertex: int) -> bool:
        return vertex in self.graph.keys()

    def get_vertices(self) -> List[Node]:
        return self.graph.keys()

    def get_neighbors(self, vertex: int) -> List:
        return self.graph[vertex]

    def get_edge_weight(self, vertex_1: int, vertex_2: int) -> int:
        for node in self.graph[vertex_1]:
            if node.index == vertex_2:
                return node.weight
        return None

    def is_connected(self):
        components = self.find_components()
        return all_equal(list(filter(lambda x: x != -1, components)))

    def calculate_distance_matrix(self) -> np.ndarray:
        dist_matrix = []

        for vertex in sorted(self.get_vertices()):
            new_row = self.find_shortest_paths(vertex)[0]
            dist_matrix.append(new_row)

        return np.array(dist_matrix)

    def find_components(self):
        def find_components_recursive(nr, v, components):
            for u in self.get_neighbors(v):
                if components[u.index] == -1:
                    components[u.index] = nr
                    find_components_recursive(nr, u.index, components)

        nr = 0
        components = [-1 for _ in self.graph]

        for v in self.graph:
            if components[v] == -1:
                nr += 1
                components[v] = nr
                find_components_recursive(nr, v, components)
        return components

    def find_shortest_paths(self, first_vertex: int) -> Tuple[List[int]]:
        if first_vertex not in self.get_vertices():
            return

        weights = [np.inf for _ in self.get_vertices()]
        previous = [None for _ in self.get_vertices()]

        weights[first_vertex] = 0
        ready_vertices = []

        while len(ready_vertices) != len(self.graph):
            temp_weights = [el if i not in ready_vertices else np.inf for i, el in enumerate(weights)]
            vertex_1 = temp_weights.index(min(temp_weights))
            ready_vertices.append(vertex_1)

            for node in self.get_neighbors(vertex_1):
                vertex_2 = node.index
                new_weight = self.get_edge_weight(vertex_1, vertex_2) + weights[vertex_1]

                if weights[vertex_2] > new_weight:
                    weights[vertex_2] = new_weight
                    previous[vertex_2] = vertex_1

        return (weights, previous)

    def find_graph_center(self) -> np.ndarray:
        dist_matrix = self.calculate_distance_matrix()
        weights_sum = list(map(lambda weights: sum(weights), dist_matrix))
        graph_center = np.where(weights_sum == min(weights_sum))[0]
        return graph_center

    def find_minimax_center(self) -> np.ndarray:
        dist_matrix = self.calculate_distance_matrix()
        farthest_vertices = list(map(lambda weights: max(weights), dist_matrix))
        minimax_center = np.where(farthest_vertices == min(farthest_vertices))[0]
        return minimax_center
