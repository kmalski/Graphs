from structures.adjacency_list import AdjacencyList
from structures.weighted_adjacency_list import WeightedAdjacencyList

import tkinter as tk
from math import cos, sin, pi
import randomcolor


def create_circle(canvas, x, y, r, outline="black", fill="white", width=1):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, outline=outline, fill=fill, width=width)


def draw_graph(canvas, graph, components=None):
    canvas.delete("all")

    if components:
        rand_color = randomcolor.RandomColor()
        colors = rand_color.generate(count=max(components), luminosity='dark')

    graph_to_draw = graph
    if not isinstance(graph, AdjacencyList):
        graph_to_draw = graph.to_adjacency_list()

    n = len(graph_to_draw.graph)
    center = (canvas.winfo_width() / 2,
              canvas.winfo_height() / 2)  # needed to convert from cartesian to screen coordinates
    r = min(center) / 1.5

    diff_angle = 2 * pi / n
    for i in range(n):
        # calculate node coordinates
        angle = diff_angle * i
        x = center[0] + r * sin(angle)
        y = center[1] - r * cos(angle)

        # drawing edges
        for neighbour in graph_to_draw.graph[i]:
            if neighbour <= i:
                continue
            neighbour_angle = diff_angle * neighbour
            neighbour_x = center[0] + r * sin(neighbour_angle)
            neighbour_y = center[1] - r * cos(neighbour_angle)

            if components:
                canvas.create_line(x, y, neighbour_x, neighbour_y, fill=colors[components[i] - 1], width=2)
            else:
                canvas.create_line(x, y, neighbour_x, neighbour_y)

        if components:
            create_circle(canvas, x, y, r * 0.2, colors[components[i] - 1], width=2)
        else:
            create_circle(canvas, x, y, r * 0.2)

        canvas.create_text(x, y, text=str(i))


def draw_graph_with_weights(canvas, graph, center_indices=None):
    canvas.delete("all")

    if not isinstance(graph, WeightedAdjacencyList):
        raise TypeError

    if center_indices is not None:
        rand_color = randomcolor.RandomColor()
        color = rand_color.generate(luminosity='dark')

    n = len(graph.graph)
    center = (canvas.winfo_width() / 2,
              canvas.winfo_height() / 2)  # needed to convert from cartesian to screen coordinates
    r = min(center) / 1.5

    diff_angle = 2 * pi / n

    padding = 7
    for i in range(n):
        # calculate node coordinates
        angle = diff_angle * i
        x = center[0] + r * sin(angle)
        y = center[1] - r * cos(angle)

        # drawing edges
        for neighbour in graph.graph[i]:
            if neighbour.index <= i:
                continue
            neighbour_angle = diff_angle * neighbour.index
            neighbour_x = center[0] + r * sin(neighbour_angle)
            neighbour_y = center[1] - r * cos(neighbour_angle)

            canvas.create_line(x, y, neighbour_x, neighbour_y)
            text_x = min(x, neighbour_x) + abs(x - neighbour_x)/2
            text_y = min(y, neighbour_y) + abs(y - neighbour_y)/2

            canvas.create_rectangle(text_x - padding, text_y - padding, text_x + padding, text_y + padding, outline="SystemButtonFace", fill="SystemButtonFace")
            canvas.create_text(text_x, text_y, text=str(neighbour.weight))

        if center_indices is not None and i in center_indices:
            create_circle(canvas, x, y, r * 0.2, color, width=3)
        else:
            create_circle(canvas, x, y, r * 0.2)

        canvas.create_text(x, y, text=str(i))


def draw_directed_graph(canvas, graph, components=None):
    canvas.delete("all")

    if components:
        rand_color = randomcolor.RandomColor()
        colors = rand_color.generate(count=max(components.values()), luminosity='dark')

    graph_to_draw = graph
    if not isinstance(graph, AdjacencyList):
        graph_to_draw = graph.to_adjacency_list()

    n = len(graph_to_draw.graph)
    center = (canvas.winfo_width() / 2,
              canvas.winfo_height() / 2)  # needed to convert from cartesian to screen coordinates
    r = min(center) / 1.5

    diff_angle = 2 * pi / n
    for i in range(n):
        # calculate node coordinates
        angle = diff_angle * i
        x = center[0] + r * sin(angle)
        y = center[1] - r * cos(angle)

        # drawing edges
        for neighbour in graph_to_draw.graph[i]:
            neighbour_angle = diff_angle * neighbour
            neighbour_x = center[0] + (r * 0.8) * sin(neighbour_angle)
            neighbour_y = center[1] - (r * 0.8) * cos(neighbour_angle)

            if components and components[i] == components[neighbour]:
                canvas.create_line(x, y, neighbour_x, neighbour_y, arrow='last', fill=colors[components[i] - 1], width=2)
            else:
                canvas.create_line(x, y, neighbour_x, neighbour_y, arrow='last')

        if components:
            create_circle(canvas, x, y, r * 0.2, colors[components[i] - 1], width=2)
        else:
            create_circle(canvas, x, y, r * 0.2)

        canvas.create_text(x, y, text=str(i))

def draw_directed_graph_with_weights(canvas, graph):
    canvas.delete("all")

    if not isinstance(graph, WeightedAdjacencyList):
        raise TypeError

    n = len(graph.graph)
    center = (canvas.winfo_width() / 2,
              canvas.winfo_height() / 2)  # needed to convert from cartesian to screen coordinates
    r = min(center) / 1.5

    diff_angle = 2 * pi / n

    padding = 7
    for i in range(n):
        # calculate node coordinates
        angle = diff_angle * i
        x = center[0] + r * sin(angle)
        y = center[1] - r * cos(angle)

        # drawing edges
        for neighbour in graph.graph[i]:
            neighbour_angle = diff_angle * neighbour.index
            neighbour_x = center[0] + (r * 0.8) * sin(neighbour_angle)
            neighbour_y = center[1] - (r * 0.8) * cos(neighbour_angle)
    
            text_x = min(x, neighbour_x) + abs(x - neighbour_x)/2
            text_y = min(y, neighbour_y) + abs(y - neighbour_y)/2

            canvas.create_line(x, y, neighbour_x, neighbour_y, arrow='last')
            canvas.create_rectangle(text_x - padding, text_y - padding, text_x + padding, text_y + padding, outline="SystemButtonFace", fill="SystemButtonFace")
            canvas.create_text(text_x, text_y, text=str(neighbour.weight))

        create_circle(canvas, x, y, r * 0.2)
        canvas.create_text(x, y, text=str(i))