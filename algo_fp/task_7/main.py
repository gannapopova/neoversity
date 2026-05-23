import random
from collections import Counter

import matplotlib.pyplot as plt


ANALYTICAL = {
    2: 1 / 36,
    3: 2 / 36,
    4: 3 / 36,
    5: 4 / 36,
    6: 5 / 36,
    7: 6 / 36,
    8: 5 / 36,
    9: 4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36,
}


def simulate(rolls: int, seed: int = 42) -> Counter:
    rng = random.Random(seed)
    counts = Counter()
    for _ in range(rolls):
        s = rng.randint(1, 6) + rng.randint(1, 6)
        counts[s] += 1
    return counts


def to_probabilities(counts: Counter, rolls: int) -> dict:
    return {s: counts[s] / rolls for s in range(2, 13)}


def print_table(probabilities: dict, rolls: int) -> None:
    print(f"\nРезультати симуляції ({rolls:,} кидків):\n".replace(",", " "))
    print(f"{'Сума':>5} | {'Монте-Карло':>14} | {'Аналітично':>12} | {'|Δ|':>10}")
    print("-" * 52)
    for s in range(2, 13):
        mc = probabilities[s]
        an = ANALYTICAL[s]
        print(f"{s:>5} | {mc * 100:>12.4f}% | {an * 100:>10.4f}% | {abs(mc - an) * 100:>8.4f}%")


def plot_probabilities(probabilities: dict, rolls: int, filename: str = "dice_probabilities.png") -> None:
    sums = list(range(2, 13))
    mc_values = [probabilities[s] * 100 for s in sums]
    an_values = [ANALYTICAL[s] * 100 for s in sums]

    x = [s - 0.2 for s in sums]
    x2 = [s + 0.2 for s in sums]

    plt.figure(figsize=(10, 6))
    plt.bar(x, mc_values, width=0.4, label=f"Монте-Карло (n={rolls:,})".replace(",", " "), color="#1296F0")
    plt.bar(x2, an_values, width=0.4, label="Аналітично", color="#F09612")
    plt.xticks(sums)
    plt.xlabel("Сума двох кубиків")
    plt.ylabel("Імовірність, %")
    plt.title("Розподіл імовірностей суми двох кубиків")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.savefig(filename)
    plt.show()


if __name__ == "__main__":
    rolls = 1_000_000
    counts = simulate(rolls)
    probabilities = to_probabilities(counts, rolls)

    print_table(probabilities, rolls)
    plot_probabilities(probabilities, rolls)
