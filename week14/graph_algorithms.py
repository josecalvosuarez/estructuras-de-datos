from collections import deque
from graph import Graph


def adjacency_list(graph):
    """
    Return the adjacency list of the graph.

    The result is the internal dictionary mapping vertices to lists
    of adjacent vertices.
    """
    return graph.adj


def adjacency_matrix(graph):
    """
    Return the adjacency matrix of the graph and its vertices.

    The result is a tuple (vertices, matrix) where:
    - vertices is a list of vertex labels.
    - matrix is a 2D list representing connections (1 = edge, 0 = none).
    """
    vertices = list(graph.adj.keys())
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    for u in graph.adj:
        for v in graph.adj[u]:
            i = index[u]
            j = index[v]
            matrix[i][j] = 1

    return vertices, matrix


def print_adjacency_matrix(graph):
    """
    Print the adjacency matrix of the graph with vertex labels,
    formatted with wider spacing for readability.
    """
    vertices, matrix = adjacency_matrix(graph)

    # print header
    header = "     " + "   ".join(str(v) for v in vertices)
    print(header)
    print("    " + "----" * len(vertices))

    # print rows
    for i, v in enumerate(vertices):
        row = "   ".join(str(x) for x in matrix[i])
        print(f"{v:>2} | {row}")


def bfs(graph, start):
    """
    Perform a breadth-first search starting at the given vertex.

    Returns the list of vertices in the order they are visited.
    """
    visited = set()
    order = []
    queue = deque()

    if start not in graph.adj:
        return order

    visited.add(start)
    queue.append(start)

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return order


def dfs(graph, start):
    """
    Perform a depth-first search starting at the given vertex.

    Returns the list of vertices in the order they are visited.
    """
    visited = set()
    order = []

    def visit(u):
        visited.add(u)
        order.append(u)
        for v in graph.adj[u]:
            if v not in visited:
                visit(v)

    if start in graph.adj:
        visit(start)

    return order


if __name__ == "__main__":
    g = Graph(directed=False)
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('C', 'D')

    print("Adjacency list:", adjacency_list(g))

    vertices, matrix = adjacency_matrix(g)
    print("Vertices:", vertices)
    print("Adjacency matrix:")
    print_adjacency_matrix(g)

    print("BFS from A:", bfs(g, 'A'))
    print("DFS from A:", dfs(g, 'A'))
