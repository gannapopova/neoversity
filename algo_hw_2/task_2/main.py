from collections import deque

def is_palindrome(text: str) -> bool:
    normalized = "".join(ch.lower() for ch in text if not ch.isspace())
    chars = deque(normalized)

    while len(chars) > 1:
        if chars.popleft() != chars.pop():
            return False
    return True

if __name__ == "__main__":
    samples = [
        "А роза упала на лапу Азора",
        "Level",
        "Was it a car or a cat I saw",
        "Hello world",
        "Не пале ленапе н",
        "",
        "a",
    ]

    for sample in samples:
        result = "так" if is_palindrome(sample) else "ні"
        print(f"'{sample}' — паліндром? {result}")
