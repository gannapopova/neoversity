import argparse
import turtle


def koch_segment(t: turtle.Turtle, length: float, level: int) -> None:
    if level == 0:
        t.forward(length)
        return
    length /= 3
    koch_segment(t, length, level - 1)
    t.left(60)
    koch_segment(t, length, level - 1)
    t.right(120)
    koch_segment(t, length, level - 1)
    t.left(60)
    koch_segment(t, length, level - 1)


def draw_snowflake(level: int, size: float = 300) -> None:
    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха (рівень {level})")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.color("blue")
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    for _ in range(3):
        koch_segment(t, size, level)
        t.right(120)

    t.hideturtle()
    screen.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Малює сніжинку Коха заданого рівня рекурсії.")
    parser.add_argument(
        "-l",
        "--level",
        type=int,
        default=None,
        help="Рівень рекурсії (ціле невід'ємне число)",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=float,
        default=300.0,
        help="Розмір сторони початкового трикутника (за замовчуванням 300)",
    )
    args = parser.parse_args()

    level = args.level
    if level is None:
        try:
            level = int(input("Введіть рівень рекурсії (ціле число >= 0): "))
        except ValueError:
            print("Рівень рекурсії має бути цілим числом.")
            return

    if level < 0:
        print("Рівень рекурсії має бути невід'ємним числом.")
        return

    draw_snowflake(level, args.size)


if __name__ == "__main__":
    main()
