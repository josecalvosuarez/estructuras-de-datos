from collections import deque
from graph import Graph


def topological_sort_dfs(graph):
    """
    Perform a topological sort of a directed acyclic graph using DFS.

    Returns a list of vertices in topological order. If the graph has
    cycles, the result is not guaranteed to be valid.
    """
    visited = set()
    order = []

    def dfs(u):
        visited.add(u)
        for v in graph.adj.get(u, []):
            if v not in visited:
                dfs(v)
        order.append(u)

    for vertex in graph.adj:
        if vertex not in visited:
            dfs(vertex)

    order.reverse()
    return order


def topological_sort_kahn(graph):
    """
    Perform a topological sort of a directed graph using Kahn's algorithm.

    Returns a list of vertices in topological order.
    If the graph contains a cycle, raises a ValueError.
    """
    indegree = {}
    for u in graph.adj:
        indegree.setdefault(u, 0)
        for v in graph.adj[u]:
            indegree[v] = indegree.get(v, 0) + 1

    queue = deque([v for v in indegree if indegree[v] == 0])
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.adj.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    if len(order) != len(indegree):
        raise ValueError("Graph has at least one cycle; topological sort is not possible.")

    return order


if __name__ == "__main__":
    g = Graph(directed=True)
    g.add_edge("A", "C")
    g.add_edge("B", "C")
    g.add_edge("C", "D")
    g.add_edge("D", "E")

    print("Topological sort (DFS):", topological_sort_dfs(g))
    print("Topological sort (Kahn):", topological_sort_kahn(g))
