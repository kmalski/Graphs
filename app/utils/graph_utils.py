from structures.adjacency_list import AdjacencyList

import random
from copy import deepcopy

def is_graphic_sequence(sequence_par: list):
    sequence = deepcopy(sequence_par)
    size = len(sequence)
    sequence.sort(reverse=True)

    while True:
        if not any(sequence):
            return True
        if sequence[0] < 0 or sequence[0] >= size or any(i < 0 for i in sequence):
            return False

        for i in range(sequence[0] + 1):
            sequence[i] -= 1

        sequence[0] = 0
        sequence.sort(reverse=True)


def randomize(adj_list: AdjacencyList):
    if not isinstance(adj_list, AdjacencyList):
        raise TypeError

    if adj_list.get_amount_of_edges() < 2:
        return 

    max_neighbors = len(adj_list.graph) - 1

    if all(len(neighbors) == max_neighbors for neighbors in adj_list.graph.values()):
        return
    
    edge_1 = adj_list.get_random_edge()

    while True:
        edge_2 = adj_list.get_random_edge()
        if sorted(edge_1) != sorted(edge_2):
            break
    
    a, b = edge_1
    c, d = edge_2

    if any(vertex in edge_1 for vertex in edge_2): 
        if a == c:
            if adj_list.does_edge_exist(b, d) == True:
                randomize(adj_list)
                return
            adj_list.add_edge(b, d)

        elif a == d:
            if adj_list.does_edge_exist(b, c) == True:
                randomize(adj_list)
                return
            adj_list.add_edge(b, c)

        elif b == c:
            if adj_list.does_edge_exist(a, d) == True:
                randomize(adj_list)
                return
            adj_list.add_edge(a, d)
            
        elif b == d:
            if adj_list.does_edge_exist(a, c) == True:
                randomize(adj_list)
                return
            adj_list.add_edge(a, c)

        if random.choice([True, False]):
            adj_list.graph[a].remove(b)
            adj_list.graph[b].remove(a)
        else:
            adj_list.graph[c].remove(d)
            adj_list.graph[d].remove(c)
            
    else: 
        if adj_list.does_edge_exist(a, d) == True or adj_list.does_edge_exist(b, c) == True:
            randomize(adj_list)
            return
            
        adj_list.graph[a].remove(b)
        adj_list.graph[b].remove(a) 
        adj_list.graph[c].remove(d)
        adj_list.graph[d].remove(c)

        adj_list.add_edge(a, d)
        adj_list.add_edge(b, c)