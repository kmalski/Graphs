import structures.adjacency_matrix as adj_matrix
import structures.incidence_matrix as inc_matrix
from utils.pythonic import all_equal

from collections import defaultdict
from dataclasses import dataclass
from copy import deepcopy
from typing import List
import numpy as np
import random


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
    def from_graphic_sequence(cls, sequence_par: list):
        graph = defaultdict(list)
        sequence = deepcopy(sequence_par)
        sequence.sort(reverse=True)
        sequence = [[sequence[i], i] for i in range(len(sequence))]  # create pairs [degree, index]

        for i in range(len(sequence)):
            graph[i]  # creating isolated nodes
            left_index = sequence[0][1]
            for j in range(sequence[0][0] + 1):
                right_index = sequence[j][1]
                if left_index == right_index:
                    continue
                graph[left_index].append(right_index)
                graph[right_index].append(left_index)
                sequence[j][0] -= 1

            sequence[0][0] = 0
            sequence.sort(reverse=True, key=lambda x: x[0])

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

    def remove_edge(self, vertex_1: int, vertex_2: int):
        self.graph[vertex_1].remove(vertex_2)
        self.graph[vertex_2].remove(vertex_1)

    def remove_vertex(self, vertex: int):
        self.graph.pop(vertex)

    def is_edge(self, vertex_1: int, vertex_2: int) -> bool:
        return vertex_1 in self.graph[vertex_2]

    def is_connected(self):
        components = self.find_components()
        return all_equal(list(filter(lambda x: x != -1, components)))

    def is_bridge(self, vertex_1, vertex_2):
        if len(self.graph[vertex_1]) == 1 or len(self.graph[vertex_2]) == 1:
            return True
        
        graph = deepcopy(self)
        graph.remove_edge(vertex_1, vertex_2)
        return not graph.is_connected()

    def get_neighbors(self, vertex: int) -> list:
        return self.graph[vertex]

    def get_amount_of_edges(self) -> int:
        amount_of_edges = sum(map(lambda neighbors: len(neighbors), self.graph.values()))
        return amount_of_edges // 2

    def get_amount_of_vertices(self) -> int:
        return len(self.graph)

    def get_random_edge(self) -> tuple:
        if self.get_amount_of_edges() == 0:
            return None

        while True:
            vertex_1, neighbors = random.choice(list(self.graph.items()))

            if len(neighbors) != 0:
                vertex_2 = random.choice(neighbors)
                return (vertex_1, vertex_2)

    def get_two_random_separated_edges(self):
        a, b = self.get_random_edge()

        for _ in range(self.get_amount_of_edges()):  # infinite loop break condition
            edge = self.get_random_edge()
            if a not in edge and b not in edge:
                return ((a, b), edge)

        return None

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

    def find_components(self):

        def find_components_recursive(nr, v, components):
            for u in self.get_neighbors(v):
                if components[u] == -1:
                    components[u] = nr
                    find_components_recursive(nr, u, components)

        nr = 0
        components = [-1 for _ in range(max(self.graph) + 1)]

        for v in self.graph:
            if components[v] == -1:
                nr += 1
                components[v] = nr
                find_components_recursive(nr, v, components)
        return components

    def find_eulerian_path(self):
        curr_vertex = 0
        next_vertex = None
        path = []

        graph = deepcopy(self)

        while len(path) != self.get_amount_of_edges():
            path.append(curr_vertex)

            neighbors = graph.get_neighbors(curr_vertex)
            non_bridges = list(filter(lambda x: not graph.is_bridge(curr_vertex, x), neighbors))

            if not non_bridges:
                next_vertex = neighbors[0]
                graph.remove_edge(curr_vertex, next_vertex)
                graph.remove_vertex(curr_vertex)
            else:
                next_vertex = non_bridges[0]
                graph.remove_edge(curr_vertex, next_vertex)

            curr_vertex = next_vertex

        path.append(curr_vertex)
        return path

    def is_hamiltonian(self, vertex: int, visited: List[int]) -> bool:
        visited.append(vertex)
        flag = False

        if len(visited) == len(self.graph):
            if vertex in self.graph[visited[0]]:
                visited.append(visited[0])
            return True
        
        for v in self.get_neighbors(vertex):
            if v not in visited:
                flag = self.is_hamiltonian(v, visited)

        if flag:
            return True

        visited.pop(-1) 


@dataclass(eq=True, order=True)
class Node:
    index: int
    weight: int


class AdjacencyListWithWeights(AdjacencyList):
    def __init__(self, graph):
        self.graph = graph

    def __str__(self):
        result = ''
        for vertex, neighbors in self.graph.items():
            result += str(vertex) + ': '
            result += ', '.join(map(str, neighbors))
            result += '\n'
        return result

    def add_edge(self, first: int, second: int, weight: int):
        if not any(neigbour.index == second for neigbour in self.graph[first]):
            self.graph[first].append(Node(second, weight))
            self.graph[second].append(Node(first, weight))
            return True
        return False

    def has_vertex(self, vertex: int) -> bool:
        return vertex in self.graph.keys()

    def get_vertices(self) -> List[Node]:
        return self.graph.keys()

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

    def get_edge_weight(self, vertex_1: int, vertex_2: int) -> int:
        for node in self.graph[vertex_1]:
            if node.index == vertex_2:
                return node.weight
        return None

    def find_shortest_paths(self, first_vertex: int) -> List[List[int]]:
        if first_vertex not in self.graph.keys():
            return

        weights = [np.inf for _ in self.graph.keys()]
        previous = [None for _ in self.graph.keys()]

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

        return [weights, previous]
