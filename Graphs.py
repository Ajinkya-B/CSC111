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
        if item1 in self._vertices and item2 in self._vertices:
            return any(item2 == vertex.item for vertex in self._vertices[item1].neighbours)
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
            return set(vertex.item for vertex in self._vertices[item].neighbours)
        else:
            raise ValueError

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
