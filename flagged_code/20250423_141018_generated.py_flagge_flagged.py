def bellman_ford(graph, source):
    """
    Finds the shortest paths from a source node to all other nodes in a graph using the Bellman-Ford algorithm.

    Args:
        graph: A dictionary representing the graph, where keys are nodes and values are lists of tuples,
               each tuple representing an edge (neighbor, weight).
        source: The source node.

    Returns:
        A tuple containing:
            - A dictionary of shortest path distances from the source to each node.
            - A dictionary of predecessors for each node in the shortest paths.
            - True if no negative cycles were detected, False otherwise.
    """
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[source] = 0

    # Relax edges repeatedly
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node]:
                if distances[node] != float('inf') and distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    predecessors[neighbor] = node

    # Check for negative cycles
    for node in graph:
        for neighbor, weight in graph[node]:
            if distances[node] != float('inf') and distances[node] + weight < distances[neighbor]:
                print("Graph contains negative cycle")
                return distances, predecessors, False

    return distances, predecessors, True

if __name__ == '__main__':
    # Example graph
    graph = {
        'A': [('B', -1), ('C', 4)],
        'B': [('C', 3), ('D', 2), ('E', 2)],
        'C': [],
        'D': [('B', 1), ('C', 5)],
        'E': [('D', -3)]
    }

    source_node = 'A'
    distances, predecessors, no_negative_cycle = bellman_ford(graph, source_node)

    if no_negative_cycle:
        print("Shortest path distances from node", source_node + ":")
        for node, distance in distances.items():
            print(f"  To {node}: {distance}")

        print("\nPredecessors in shortest paths:")
        for node, predecessor in predecessors.items():
            print(f"  Node {node}: Predecessor {predecessor}")

    # Example with a negative cycle
    graph_negative_cycle = {
        'A': [('B', -1)],
        'B': [('C', -2)],
        'C': [('A', -3)]
    }

    source_node_negative = 'A'
    distances_negative, predecessors_negative, no_negative_cycle_negative = bellman_ford(graph_negative_cycle, source_node_negative)