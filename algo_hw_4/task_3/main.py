import random
import sys
import timeit


sys.setrecursionlimit(20000)


def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    a = arr[:]
    _merge_sort_inplace(a, 0, len(a) - 1)
    return a


def _merge_sort_inplace(a, left, right):
    if left >= right:
        return
    mid = (left + right) // 2
    _merge_sort_inplace(a, left, mid)
    _merge_sort_inplace(a, mid + 1, right)
    _merge(a, left, mid, right)


def _merge(a, left, mid, right):
    left_part = a[left:mid + 1]
    right_part = a[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            a[k] = left_part[i]
            i += 1
        else:
            a[k] = right_part[j]
            j += 1
        k += 1
    while i < len(left_part):
        a[k] = left_part[i]
        i += 1
        k += 1
    while j < len(right_part):
        a[k] = right_part[j]
        j += 1
        k += 1


def timsort_builtin(arr):
    return sorted(arr)


def generate_datasets(size):
    random_data = [random.randint(0, size) for _ in range(size)]
    sorted_data = list(range(size))
    reversed_data = list(range(size, 0, -1))
    nearly_sorted = list(range(size))
    for _ in range(max(1, size // 100)):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        nearly_sorted[i], nearly_sorted[j] = nearly_sorted[j], nearly_sorted[i]
    return {
        "випадковий": random_data,
        "відсортований": sorted_data,
        "обернений": reversed_data,
        "майже відсортований": nearly_sorted,
    }


def measure(func, data, repeats):
    timer = timeit.Timer(lambda: func(data))
    return timer.timeit(number=repeats) / repeats


def run_benchmark():
    sizes = [1000, 5000, 10000]
    algorithms = {
        "Insertion sort": insertion_sort,
        "Merge sort": merge_sort,
        "Timsort (sorted)": timsort_builtin,
    }

    overall = {name: 0.0 for name in algorithms}

    for size in sizes:
        print(f"\n=== Розмір масиву: {size} ===")
        datasets = generate_datasets(size)

        for ds_name, data in datasets.items():
            print(f"\n  Набір: {ds_name}")
            repeats = 1 if size >= 5000 else 3
            for algo_name, func in algorithms.items():
                if algo_name == "Insertion sort" and size > 5000 and ds_name != "відсортований":
                    print(f"    {algo_name:<18} | пропущено (надто повільно для n={size})")
                    continue
                t = measure(func, data, repeats)
                overall[algo_name] += t
                print(f"    {algo_name:<18} | {t * 1000:10.3f} мс")

    print("\n=== Сумарний час по всіх запусках (без пропусків) ===")
    for name, total in sorted(overall.items(), key=lambda kv: kv[1]):
        print(f"  {name:<18} | {total * 1000:10.3f} мс")


if __name__ == "__main__":
    run_benchmark()
