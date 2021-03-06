"""
This file goes over some of the methods we used to work with Graphs.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Ajinkya Bhosale.
"""

from __future__ import annotations
from typing import Any


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
       - item: The data stored in this vertex.
       - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
      - self not in self.neighbours
      - all(self in vertex.neighbours for vertex in self.neighbours)
    """
    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

    def print_all_connected(self, visited: set[_Vertex]) -> None:
        """Print all items that this vertex is connected to, WITHOUT using any of the vertices
        in visited.

        Preconditions:
            - self not in visited
        """
        print(self.item)
        visited.add(self)
        for neighbour in self.neighbours:
            if neighbour not in visited:
                neighbour.print_all_connected(visited)

    def print_all_connected_indented(self, visited: set[_Vertex], d: int) -> None:
        """Print all items that this vertex is connected to, WITHOUT using any of the vertices
        in visited.

        Print out the items with indentation level d

        Preconditions:
            - self not in visited
        """
        print(' ' * d, self.item)
        visited.add(self)
        for neighbour in self.neighbours:
            if neighbour not in visited:
                neighbour.print_all_connected_indented(visited, d + 1)

    def spanning_tree(self, visited: set[_Vertex]) -> list[set]:
        """Return a spanning tree for all items this vertex is connected to,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """

        visited.add(self)
        edges_so_far = []

        for neighbour in self.neighbours:
            if neighbour not in visited:
                edge = {self.item, neighbour.item}
                edges_so_far.append(edge)

                edges_so_far.extend(neighbour.spanning_tree(visited))

        return edges_so_far

    def check_connected(self, target_item: Any, visited: set[_Vertex]) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """

        if self.item == target_item:
            return True
        else:
            visited.add(self)
            for v in self.neighbours:
                if v not in visited:
                    if v.check_connected(target_item, visited):
                        return True
            return False


class Graph:
    """A graph."""
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        # Checking if the inputted items are even a vertex in the current graph
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.

        Sample Usage:
        >>> graph = create_sample_graph()
        >>> graph.adjacent(7, 6) # at least one item not in the graph
        False
        >>> graph.adjacent(5, 4)
        True
        >>> graph.adjacent(4, 6) # both items in a graph, but are not neighbours
        False
        """
        # Checking if the inputted items are even a vertex in the current graph
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.

        Sample Usage:

        >>> graph = create_sample_graph()
        >>> graph.get_neighbours(4) == {5, 2}
        True
        >>> graph.get_neighbours(5) == {4}
        True
        """
        if item in self._vertices:
            v1 = self._vertices[item]
            return {neighbour.item for neighbour in v1.neighbours}
        else:
            raise ValueError

    def num_edges(self) -> int:
        """Return the number of edges in this graph.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_vertex(4)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.num_edges()
        2
        >>> g.add_edge(1, 3)
        >>> g.num_edges()
        3
        """
        sum_so_far = 0
        for v in self._vertices.values():
            sum_so_far += len(v.neighbours)

        return sum_so_far // 2

    def connected(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are connected vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_vertex(4)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.connected(1, 3)
        True
        >>> g.connected(1, 4)
        False
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return v1.check_connected(item2, set())  # Pass in an empty "visited" set
        else:
            return False

    def spanning_tree(self) -> list[set]:
        """Return a subset of the edges of this graph that form a spanning tree.

        The edges are returned as a list of sets, where each set contains the two
        ITEMS corresponding to an edge. Each returned edge is in this graph
        (i.e., this function doesn't create new edges!).

        Preconditions:
            - this graph is connected
        """

        # get a starting vertex
        return self._vertices[0].spanning_tree(set())


def complete_graph(n: int) -> Graph:
    """Return a graph of n vertices where all pairs of vertices are adjacent.

    The vertex items are the numbers 0 through n - 1, inclusive.

    Preconditions:
        - n >= 0
    """
    graph = Graph()

    for v in range(n):
        graph.add_vertex(v)
        for u in range(v):
            graph.add_edge(v, u)

    return graph


def create_sample_graph() -> Graph:
    graph = Graph()
    for item in [5, 4, 2, 6]:
        graph.add_vertex(item)
    graph.add_edge(4, 5)
    graph.add_edge(4, 2)
    graph.add_edge(6, 2)

    return graph
