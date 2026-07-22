import heapq

def dijkstra(graph, start, end):
    """
    Finds the shortest path between start and end using Dijkstra's Algorithm.

    Parameters:
        graph : dict
            {
                node: [(neighbor, distance), ...]
            }

        start : int
            Starting node ID

        end : int
            Destination node ID

    Returns:
        (path, total_distance)

        path -> list of node IDs
        total_distance -> distance in meters
    """

    # Distance from start to every node
    distances = {}

    # Previous node for path reconstruction
    previous = {}

    # Initialize
    for node in graph:
        distances[node] = float("inf")
        previous[node] = None

    distances[start] = 0

    # Priority queue (distance, node)
    priority_queue = [(0, start)]

    visited = set()

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if already processed
        if current_node in visited:
            continue

        visited.add(current_node)

        # Stop when destination is reached
        if current_node == end:
            break

        # Explore neighbors
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in distances:
                distances[neighbor] = float("inf")
                previous[neighbor] = None
                
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # No path exists
    if distances[end] == float("inf"):
        return None, None

    # Reconstruct shortest path
    path = []

    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[end]