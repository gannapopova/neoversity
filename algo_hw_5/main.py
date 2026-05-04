import timeit
from pathlib import Path


def boyer_moore(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    bad_char = {ch: i for i, ch in enumerate(pattern)}

    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        shift = j - bad_char.get(text[s + j], -1)
        s += max(1, shift)
    return -1


def kmp(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    lps = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = lps[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        lps[i] = k

    q = 0
    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = lps[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            return i - m + 1
    return -1


def rabin_karp(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    base = 256
    mod = 10 ** 9 + 7

    high_order = pow(base, m - 1, mod)
    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if pattern_hash == window_hash and text[i:i + m] == pattern:
            return i
        if i < n - m:
            window_hash = (
                (window_hash - ord(text[i]) * high_order) * base + ord(text[i + m])
            ) % mod
    return -1


def measure(func, text, pattern, number=5):
    timer = timeit.Timer(lambda: func(text, pattern))
    return timer.timeit(number=number) / number


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8").lstrip("﻿")


def benchmark(name: str, text: str, existing: str, fake: str):
    print(f"\n=== {name} (довжина: {len(text)} символів) ===")
    print(f"Існуючий підрядок: '{existing}'")
    print(f"Вигаданий підрядок: '{fake}'")

    algorithms = {
        "Боєра-Мура": boyer_moore,
        "Кнута-Морріса-Пратта": kmp,
        "Рабіна-Карпа": rabin_karp,
    }

    results = {"existing": {}, "fake": {}}
    for algo_name, func in algorithms.items():
        t_exist = measure(func, text, existing)
        t_fake = measure(func, text, fake)
        results["existing"][algo_name] = t_exist
        results["fake"][algo_name] = t_fake
        print(
            f"  {algo_name:<22} | існуючий: {t_exist * 1000:8.4f} мс "
            f"| вигаданий: {t_fake * 1000:8.4f} мс"
        )

    fastest_exist = min(results["existing"], key=results["existing"].get)
    fastest_fake = min(results["fake"], key=results["fake"].get)
    print(f"  -> найшвидший на існуючому: {fastest_exist}")
    print(f"  -> найшвидший на вигаданому: {fastest_fake}")
    return results


def main():
    base = Path(__file__).parent
    article_1 = load(base / "article_1.txt")
    article_2 = load(base / "article_2.txt")

    existing_1 = "алгоритм"
    fake_1 = "квантовий деструктор"

    existing_2 = "рекомендаційної системи"
    fake_2 = "блокчейн-нейромережа"

    res_1 = benchmark("Стаття 1", article_1, existing_1, fake_1)
    res_2 = benchmark("Стаття 2", article_2, existing_2, fake_2)

    print("\n=== Загальний підсумок ===")
    totals = {algo: 0.0 for algo in res_1["existing"]}
    for res in (res_1, res_2):
        for algo, t in res["existing"].items():
            totals[algo] += t
        for algo, t in res["fake"].items():
            totals[algo] += t

    for algo, t in sorted(totals.items(), key=lambda kv: kv[1]):
        print(f"  {algo:<22} | сумарний час: {t * 1000:8.4f} мс")

    fastest_overall = min(totals, key=totals.get)
    print(f"\nНайшвидший алгоритм у цілому: {fastest_overall}")


if __name__ == "__main__":
    main()
