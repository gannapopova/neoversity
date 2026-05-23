import heapq


def dijkstra(graph: dict, start) -> tuple[dict, dict]:
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}

    heap = [(0, start)]
    visited = set()

    while heap:
        current_dist, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)

        if current_dist > distances[current]:
            continue

        for neighbor, weight in graph[current].items():
            if neighbor in visited:
                continue
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))

    return distances, previous


def reconstruct_path(previous: dict, start, end) -> list:
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    if path[0] != start:
        return []
    return path


if __name__ == "__main__":
    graph = {
        "A": {"B": 5, "C": 1},
        "B": {"A": 5, "C": 2, "D": 1},
        "C": {"A": 1, "B": 2, "D": 4, "E": 8},
        "D": {"B": 1, "C": 4, "E": 3, "F": 6},
        "E": {"C": 8, "D": 3, "F": 2},
        "F": {"D": 6, "E": 2},
    }

    start = "A"
    distances, previous = dijkstra(graph, start)

    print(f"Найкоротші відстані від '{start}':")
    for node in sorted(distances):
        path = reconstruct_path(previous, start, node)
        print(f"  до {node}: відстань = {distances[node]}, шлях = {' -> '.join(path)}")
