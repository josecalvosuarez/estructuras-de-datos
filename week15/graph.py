class Graph:
    """
    Simple graph represented as a dictionary where each key is a vertex
    and the value is a list of adjacent vertices.
    """

    def __init__(self, directed=False):
        """
        Create an empty graph.

        If directed is False, edges are added in both directions.
        """
        self.directed = directed
        self.adj = {}

    def add_vertex(self, v):
        """Add a vertex to the graph if it is not already present."""
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u, v):
        """
        Add an edge from u to v.

        If the graph is undirected, an edge from v to u is also added.
        """
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def vertices(self):
        """Return a list of vertices in the graph."""
        return list(self.adj.keys())

    def edges(self):
        """
        Return a list of edges in the graph.

        For a directed graph, edges are ordered pairs (u, v).
        For an undirected graph, each edge appears only once.
        """
        edge_list = []
        seen = set()
        for u in self.adj:
            for v in self.adj[u]:
                if self.directed:
                    edge_list.append((u, v))
                else:
                    if (v, u) not in seen:
                        edge_list.append((u, v))
                        seen.add((u, v))
        return edge_list

    def pretty_print(self):
        """
        Print the adjacency list of the graph in a readable format.
        """
        print("Graph (directed={})".format(self.directed))
        for v in self.adj:
            neighbors = ", ".join(str(n) for n in self.adj[v])
            print("{} -> {}".format(v, neighbors))

    def __str__(self):
        """
        Return a string representation of the graph adjacency list.
        """
        lines = ["Graph (directed={})".format(self.directed)]
        for v in self.adj:
            neighbors = ", ".join(str(n) for n in self.adj[v])
            lines.append("{} -> {}".format(v, neighbors))
        return "\n".join(lines)


if __name__ == "__main__":
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    g.pretty_print()
