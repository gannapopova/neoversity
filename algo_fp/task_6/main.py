items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict, budget: int) -> dict:
    sorted_items = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )
    chosen = []
    total_cost = 0
    total_calories = 0
    for name, props in sorted_items:
        if total_cost + props["cost"] <= budget:
            chosen.append(name)
            total_cost += props["cost"]
            total_calories += props["calories"]
    return {"items": chosen, "total_cost": total_cost, "total_calories": total_calories}


def dynamic_programming(items: dict, budget: int) -> dict:
    names = list(items.keys())
    n = len(names)

    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        cal = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]
            if cost <= b:
                with_item = dp[i - 1][b - cost] + cal
                if with_item > dp[i][b]:
                    dp[i][b] = with_item

    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]
    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = dp[n][budget]
    return {"items": chosen, "total_cost": total_cost, "total_calories": total_calories}


if __name__ == "__main__":
    for budget in [50, 75, 100, 150]:
        print(f"\nБюджет: {budget}")
        g = greedy_algorithm(items, budget)
        d = dynamic_programming(items, budget)
        print(
            f"  Жадібний: {g['items']}, "
            f"вартість = {g['total_cost']}, калорій = {g['total_calories']}"
        )
        print(
            f"  ДП:       {d['items']}, "
            f"вартість = {d['total_cost']}, калорій = {d['total_calories']}"
        )
