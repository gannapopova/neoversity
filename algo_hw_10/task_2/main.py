import random
import numpy as np
import scipy.integrate as spi

def f(x):
    return x ** 2

A = 0.0
B = 2.0

def monte_carlo_integrate(func, a: float, b: float, n: int = 100_000, seed: int = 42) -> float:
    rng = random.Random(seed)
    y_max = max(func(a), func(b))
    sample_xs = [a + (b - a) * i / 99 for i in range(100)]
    for x in sample_xs:
        if func(x) > y_max:
            y_max = func(x)

    if y_max <= 0:
        return 0.0

    under = 0
    for _ in range(n):
        x = rng.uniform(a, b)
        y = rng.uniform(0, y_max)
        if y <= func(x):
            under += 1

    rectangle_area = (b - a) * y_max
    return rectangle_area * under / n

def monte_carlo_mean_value(func, a: float, b: float, n: int = 100_000, seed: int = 42) -> float:
    rng = random.Random(seed)
    total = 0.0
    for _ in range(n):
        x = rng.uniform(a, b)
        total += func(x)
    return (b - a) * total / n

def try_plot():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n[!] matplotlib не встановлено — графік пропущено.")
        return

    x = np.linspace(-0.5, 2.5, 400)
    y = f(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, "r", linewidth=2)

    ix = np.linspace(A, B)
    iy = f(ix)
    ax.fill_between(ix, iy, color="gray", alpha=0.3)

    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axvline(x=A, color="gray", linestyle="--")
    ax.axvline(x=B, color="gray", linestyle="--")
    ax.set_title(f"Графік інтегрування f(x) = x^2 від {A} до {B}")
    plt.grid()
    plt.savefig("integral_plot.png")
    print("[+] Графік збережено у integral_plot.png")

def main():
    analytical = (B ** 3 - A ** 3) / 3
    quad_result, quad_error = spi.quad(f, A, B)

    print(f"Функція: f(x) = x^2,  межі [{A}, {B}]\n")
    print(f"Аналітичне значення:      {analytical:.10f}")
    print(f"scipy.integrate.quad:     {quad_result:.10f} (похибка ≈ {quad_error:.2e})\n")

    print("Метод Монте-Карло (метод відкидання — точки під кривою):")
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        mc = monte_carlo_integrate(f, A, B, n=n)
        err = abs(mc - quad_result)
        print(f"  n = {n:>8} -> {mc:.6f}  (|похибка| = {err:.6f})")

    print("\nМетод Монте-Карло (метод середнього значення):")
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        mc = monte_carlo_mean_value(f, A, B, n=n)
        err = abs(mc - quad_result)
        print(f"  n = {n:>8} -> {mc:.6f}  (|похибка| = {err:.6f})")

    try_plot()

if __name__ == "__main__":
    main()
