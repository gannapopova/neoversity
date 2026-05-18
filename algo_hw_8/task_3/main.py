import heapq


def min_cable_merge_cost(cables):
    if len(cables) <= 1:
        return 0

    heap = list(cables)
    heapq.heapify(heap)

    total_cost = 0
    while len(heap) > 1:
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)
        merged = first + second
        total_cost += merged
        heapq.heappush(heap, merged)

    return total_cost


if __name__ == "__main__":
    examples = [
        [4, 3, 2, 6],
        [8, 4, 6, 12],
        [1, 2, 3, 4, 5],
        [10],
        [],
    ]

    for cables in examples:
        cost = min_cable_merge_cost(cables)
        print(f"Кабелі: {cables} -> мінімальні витрати: {cost}")
