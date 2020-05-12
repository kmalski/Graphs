import structures.adjacency_list as adj_list
from utils.pythonic import all_equal

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Dict
from copy import deepcopy
import networkx as nx
import numpy as np
import random
import math


@dataclass(eq=True, order=True, frozen=True)
class Node:
    index: int
    x: int
    y: int

    def __str__(self):
        return f'({self.index}, x = {self.x}, y = {self.y})'


class CoordinatedAdjacencyList:
    def __init__(self, graph):
        self.graph = graph

    @classmethod
    def init_empty(cls):
        return cls(defaultdict(list))

    @classmethod
    def from_file(cls, file_path: str):
        graph = defaultdict(list)

        with open(file_path) as file:
            data_string = file.read()

            index = 0
            for line in iter(data_string.splitlines()):
                line = line.split()
                x = int(line[0])
                y = int(line[1])

                if index != 0:
                    previous_node = current_node
                    current_node = Node(index, x, y)
                    graph[previous_node].append(current_node)
                    graph[current_node].append(previous_node)
                else:
                    current_node = Node(index, x, y)
                index += 1

            first_node = list(graph.keys())[0]
            graph[current_node].append(first_node)
            graph[first_node].append(current_node)

        return cls(graph)

    def add_edge(self, first_vertex: Node, second_vertex: Node):
        self.graph[first_vertex].append(second_vertex)
        self.graph[second_vertex].append(first_vertex)

    def remove_edge(self, first_vertex: Node, second_vertex: Node):
        self.graph[first_vertex].remove(second_vertex)
        self.graph[second_vertex].remove(first_vertex)

    def get_vertices(self) -> List[Node]:
        return self.graph.keys()

    def to_networkX(self) -> nx.Graph:
        visualization = nx.Graph()

        for vertex in self.get_vertices():
            visualization.add_node(vertex.index, pos=(vertex.x, vertex.y))

        for start_vertex, end_vertexes in self.graph.items():
            for end_vertex in end_vertexes:
                visualization.add_edge(start_vertex.index, end_vertex.index)
        return visualization

    def calculate_path_length(self) -> float:
        length = 0
        previous_vertex = None
        for start_vertex, vertexes in self.graph.items():
            end_vertex = vertexes[0] if vertexes[0] != previous_vertex else vertexes[1]
            previous_vertex = start_vertex
            length += math.sqrt((start_vertex.x - end_vertex.x)**2 + (start_vertex.y - end_vertex.y)**2)

        return length

    def simulated_annealing(self, max_it: int):
        for i in range(100, 0, -1):
            t = 0.001 * i * i

            for _ in range(max_it):
                new_graph = CoordinatedAdjacencyList(deepcopy(self.graph))
                while True:
                    a = random.choice(list(self.get_vertices()))
                    b = random.choice(self.graph[a])
                    c = random.choice(list(self.get_vertices()))
                    d = random.choice(self.graph[c])
                    if a != c and a != d and b != c and b != d and c not in self.graph[a] and d not in self.graph[b]:
                        break

                new_graph.remove_edge(a, b)
                new_graph.add_edge(a, c)
                new_graph.remove_edge(c, d)
                new_graph.add_edge(b, d)

                old_graph_length = self.calculate_path_length()
                new_graph_length = new_graph.calculate_path_length()
                if new_graph_length < old_graph_length:
                    self.graph = new_graph.graph
                else:
                    r = random.random()
                    if r < math.exp(-(new_graph_length - old_graph_length) / t):
                        self.graph = new_graph.graph
