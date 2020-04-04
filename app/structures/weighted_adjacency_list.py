import structures.adjacency_list as adj_list
from utils.pythonic import all_equal

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Dict
from copy import deepcopy
import numpy as np
import random

@dataclass(eq=True, order=True)
class Node:
    index: int
    weight: int

    def __str__(self):
        return f'(index = {self.index}, weight = {self.weight})' 


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

    def get_graph_items(self) -> Tuple[int, List[Node]]:
        return self.graph.items()

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
        '''Dijkstra's algorithm'''

        if first_vertex not in self.graph.keys():
            raise ValueError

        distance = [np.inf for _ in self.graph.keys()]
        previous = [None for _ in self.graph.keys()]

        distance[first_vertex] = 0
        ready_vertices = []

        while len(ready_vertices) != len(self.graph):
            temp_distance = [el if i not in ready_vertices else np.inf for i, el in enumerate(distance)]
            vertex_1 = temp_distance.index(min(temp_distance))
            ready_vertices.append(vertex_1)

            for node in self.get_neighbors(vertex_1):
                vertex_2 = node.index
                new_distance = self.get_edge_weight(vertex_1, vertex_2) + distance[vertex_1]

                if distance[vertex_2] > new_distance:
                    distance[vertex_2] = new_distance
                    previous[vertex_2] = vertex_1

        return (distance, previous)

    def find_graph_center(self) -> np.ndarray:
        dist_matrix = self.calculate_distance_matrix()
        weights_sum = list(map(lambda weights: sum(weights), dist_matrix))
        graph_center = np.where(weights_sum == min(weights_sum))[0]
        return graph_center

    def find_minimal_tree(self):

        visited = [0]
        temp_graph = deepcopy(self.graph)
        number_of_nodes = len(self.graph)
        minimal_tree = WeightedAdjacencyList.init_empty()

        min_visited = 0
        min_index = np.inf
        min_weight = np.inf

        while len(visited) < number_of_nodes:
            for i in visited:
                for node in temp_graph[i]:
                    if not any(visited_node == node.index for visited_node in visited):
                        if node.weight < min_weight:
                            min_index = node.index
                            min_weight = node.weight
                            min_visited = i
            visited.append(min_index)
            minimal_tree.add_edge(min_index, min_visited, min_weight)
            for i, o in enumerate(temp_graph[min_visited]):
                if o.weight == min_weight:
                    del temp_graph[min_visited][i]
                    break
            min_weight = np.inf

        return minimal_tree

    def find_minimax_center(self) -> np.ndarray:
        dist_matrix = self.calculate_distance_matrix()
        farthest_vertices = list(map(lambda weights: max(weights), dist_matrix))
        minimax_center = np.where(farthest_vertices == min(farthest_vertices))[0]
        return minimax_center


class WeightedDirectedAdjacencyList(WeightedAdjacencyList):
    def __init__(self, graph):
        self.graph = graph

    @classmethod
    def from_directed_adj_list(cls, directed_adj_list, randomMin: int, randomMax: int):
        if not isinstance(directed_adj_list, adj_list.DirectedAdjacencyList):
            raise TypeError

        graph = defaultdict(list)

        for vertex, neighbors in directed_adj_list.get_graph_items():
            graph[vertex] #creating isolated nodes

            for neighbor in neighbors:
                graph[vertex].append(Node(neighbor, random.randint(randomMin, randomMax)))
        
        return cls(graph)

    def to_directed_adjacency_list(self):
        adjacency_list = adj_list.DirectedAdjacencyList.init_empty()

        for vertex, neighbors in self.graph.items():
            neighbor_list = [v.index for v in neighbors]
            adjacency_list.set_neighbors(vertex, neighbor_list)

        return adjacency_list
        
    def add_edge(self, vertex_from: int, vertex_to: int, weight: int) -> bool:
        if not any(neigbour.index == vertex_to for neigbour in self.graph[vertex_from]):
            self.graph[vertex_from].append(Node(vertex_to, weight))
            return True
        return False
    
    def set_edge_weight(self, vertex_from: int, vertex_to: int, weight: int) -> bool:
        for neighbour in self.graph[vertex_from]:
            if neighbour.index == vertex_to:
                neighbour.weight = weight
                return True
        return False

    def set_random_weights(self, randomMin: int, randomMax: int):
        for neighbors in self.graph.values():
            for neighbor in neighbors:
                neighbor.weight = random.randint(randomMin, randomMax) 
    
    def remove_vertex(self, vertex: int):
        for vertices in self.graph.values():
            for node in vertices:
                if node.index == vertex:
                    vertices.remove(node)

        self.graph.pop(vertex)
    
    def has_negative_cycle(self) -> bool:
        temp_graph = deepcopy(self)

        source = len(self.graph)
        for vertex in self.graph.keys():
            temp_graph.add_edge(source, vertex, 0)

        return temp_graph.find_shortest_paths(source) is None

    def find_shortest_paths(self, first_vertex: int) -> List[int]: 
        '''Bellman-Ford's algorithm'''

        if first_vertex not in self.graph.keys():
            raise ValueError

        distance = [np.inf for _ in self.graph.keys()]
        distance[first_vertex] = 0

        for _ in range(len(self.graph.keys()) - 1):
            for vertex_1, neighbours in self.graph.items():
                for neighbour in neighbours:
                    vertex_2 = neighbour.index
                    new_distance = self.get_edge_weight(vertex_1, vertex_2) + distance[vertex_1]

                    if distance[vertex_2] > new_distance: 
                        distance[vertex_2] = new_distance 

        for vertex_1, neighbours in self.graph.items():
            for neighbour in neighbours:
                vertex_2 = neighbour.index
                if distance[vertex_2] > self.get_edge_weight(vertex_1, vertex_2) + distance[vertex_1]:
                    return None

        return distance

    def calculate_distance_matrix(self) -> np.ndarray:   
        '''Johnson's algorithm'''

        temp_graph = deepcopy(self)

        source = len(self.graph)
        for vertex in self.graph.keys():
            temp_graph.add_edge(source, vertex, 0)

        h = temp_graph.find_shortest_paths(source)
        
        if not h:
            return None
        else:
            for vertex_1, neighbours in temp_graph.get_graph_items():
                for neighbour in neighbours:
                    vertex_2 = neighbour.index
                    new_weight = temp_graph.get_edge_weight(vertex_1, vertex_2) + h[vertex_1] - h[vertex_2]
                    temp_graph.set_edge_weight(vertex_1, vertex_2, new_weight)
            
            size = len(self.graph)
            dist_matrix = np.full((size, size), None)
            temp_graph.remove_vertex(source)

            for vertex_1 in temp_graph.get_vertices():
                dijkstra_distance, _ = super(WeightedDirectedAdjacencyList, temp_graph).find_shortest_paths(vertex_1)
                for vertex_2 in temp_graph.get_vertices():
                    dist_matrix[vertex_1, vertex_2] = dijkstra_distance[vertex_2] - h[vertex_1] + h[vertex_2]
            
            return dist_matrix
            