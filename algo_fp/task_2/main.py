import argparse
import math
import turtle


def pythagoras_tree(t: turtle.Turtle, length: float, level: int) -> None:
    if level == 0 or length < 1:
        return

    t.forward(length)

    t.left(45)
    pythagoras_tree(t, length * math.sqrt(2) / 2, level - 1)
    t.right(90)
    pythagoras_tree(t, length * math.sqrt(2) / 2, level - 1)
    t.left(45)

    t.backward(length)


def draw_tree(level: int, length: float = 100) -> None:
    screen = turtle.Screen()
    screen.title(f"Дерево Піфагора (рівень {level})")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.color("forestgreen")
    t.left(90)
    t.penup()
    t.goto(0, -200)
    t.pendown()

    pythagoras_tree(t, length, level)

    t.hideturtle()
    screen.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Малює фрактал «дерево Піфагора».")
    parser.add_argument("-l", "--level", type=int, default=None, help="Рівень рекурсії (>= 0)")
    parser.add_argument("-s", "--length", type=float, default=100.0, help="Довжина стовбура")
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

    draw_tree(level, args.length)


if __name__ == "__main__":
    main()
