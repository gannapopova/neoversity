import timeit

COINS = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(amount: int, coins=COINS) -> dict:
    result = {}
    for coin in sorted(coins, reverse=True):
        if amount <= 0:
            break
        count, amount = divmod(amount, coin)
        if count:
            result[coin] = count
    return result

def find_min_coins(amount: int, coins=COINS) -> dict:
    if amount < 0:
        raise ValueError("Сума не може бути від'ємною")
    if amount == 0:
        return {}

    dp = [float("inf")] * (amount + 1)
    last_coin = [0] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                last_coin[i] = coin

    if dp[amount] == float("inf"):
        return {}

    result = {}
    remaining = amount
    while remaining > 0:
        coin = last_coin[remaining]
        result[coin] = result.get(coin, 0) + 1
        remaining -= coin
    return dict(sorted(result.items()))

def benchmark(amounts, repeats=5):
    print(f"\n{'Сума':>10} | {'Жадібний, мс':>15} | {'ДП, мс':>15}")
    print("-" * 50)
    for amount in amounts:
        t_greedy = timeit.Timer(lambda: find_coins_greedy(amount)).timeit(number=repeats) / repeats
        t_dp = timeit.Timer(lambda: find_min_coins(amount)).timeit(number=repeats) / repeats
        print(f"{amount:>10} | {t_greedy * 1000:>15.4f} | {t_dp * 1000:>15.4f}")

if __name__ == "__main__":
    sample = 113
    print(f"Сума {sample}:")
    print(f"  Жадібний: {find_coins_greedy(sample)}")
    print(f"  ДП:       {find_min_coins(sample)}")

    print("\nПорівняння часу виконання:")
    benchmark([113, 1_000, 10_000, 100_000])
