"""
Test cases for turtle creation.
"""

import pytest

from ..turtle import Turtle, Screen


def test_turtle_creation():
    """
    Check turtle basic properties are set.
    """
    turtle = Turtle()

    assert turtle.pen is True


def test_turtle_forward():
    """
    Check turtle forward method.
    """
    turtle = Turtle()

    assert turtle.x == Screen.WIDTH / 2
    assert turtle.y == Screen.HEIGHT / 2

    turtle.forward(80)

    assert turtle.x == Screen.WIDTH / 2 + 80
    assert turtle.y == Screen.HEIGHT / 2

    turtle.right(90)
    turtle.forward(80)

    assert turtle.x == Screen.WIDTH / 2 + 80
    assert turtle.y == Screen.HEIGHT / 2 + 80


def test_turtle_backward():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.x == Screen.WIDTH / 2
    assert turtle.y == Screen.HEIGHT / 2

    turtle.backward(80)

    assert turtle.x == Screen.WIDTH / 2 - 80
    assert turtle.y == Screen.HEIGHT / 2

    turtle.right(90)
    turtle.backward(80)

    assert turtle.x == Screen.WIDTH / 2 - 80
    assert turtle.y == Screen.HEIGHT / 2 - 80


def test_turtle_right():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.heading() == 0

    turtle.right(90)

    assert turtle.heading() == 270

    turtle.right(360)

    assert turtle.heading() == 270


def test_turtle_left():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.heading() == 0

    turtle.left(90)

    assert turtle.heading() == 90

    turtle.right(360)

    assert turtle.heading() == 90


def test_turtle_goto():
    """
    Check turtle goto method.
    """
    turtle = Turtle()

    turtle.forward(10)
    turtle.goto(0, 0)

    assert turtle.x == Screen.WIDTH / 2
    assert turtle.y == Screen.HEIGHT / 2

    turtle = Turtle()

    turtle.forward(10)
    turtle.goto((0, 0))

    assert turtle.x == Screen.WIDTH / 2
    assert turtle.y == Screen.HEIGHT / 2


def test_turtle_teleport():
    """
    Check turtle teleport method.
    """
    turtle = Turtle()
    turtle.forward(10)
    turtle.teleport(0, 0)

    assert turtle.x == Screen.WIDTH / 2
    assert turtle.y == Screen.HEIGHT / 2


def test_turtle_dot():
    """
    Check turtle dot method.
    """
    turtle = Turtle()

    turtle.dot()

    assert turtle.screen.action["radius"] == 2.5

    turtle.dot(50)

    assert turtle.screen.action["radius"] == 25

    turtle.dot(50, "blue")

    assert turtle.screen.action["color"] == "blue"
    assert turtle.screen.action["radius"] == 25

    turtle.dot(50, (255, 0, 0))

    assert turtle.screen.action["color"] == "#ff0000"
    assert turtle.screen.action["radius"] == 25


def test_turtle_towards():
    """
    Check turtle towards, pos and setheading method.
    """
    turtle = Turtle()

    turtle.forward(10)
    turtle.setheading(turtle.towards(0, 0))
    turtle.fd(10)

    assert turtle.x == Screen.WIDTH / 2
    assert turtle.y == Screen.HEIGHT / 2
    assert abs(turtle.pos()[0]) < 1e-5
    assert abs(turtle.pos()[1]) < 1e-5

    turtle = Turtle()

    turtle.left(20)
    turtle.forward(10)
    turtle.setheading(turtle.towards((0, 0)))
    turtle.fd(10)

    assert turtle.x == Screen.WIDTH / 2
    assert turtle.y == Screen.HEIGHT / 2
    assert abs(turtle.pos()[0]) < 1e-5
    assert abs(turtle.pos()[1]) < 1e-5


def test_turtle_write():
    """
    Check turtle write texts.
    """
    turtle = Turtle()

    turtle.write("hello world")

    assert turtle.screen.action["text"] == "hello world"
    assert turtle.screen.action["align"] == "left"
    assert turtle.screen.action["font"] == ("Arial", 8, "normal")

    turtle = Turtle()

    turtle.write("hello world", "right")

    assert turtle.screen.action["text"] == "hello world"
    assert turtle.screen.action["align"] == "right"
    assert turtle.screen.action["font"] == ("Arial", 8, "normal")

    turtle = Turtle()
    turtle.write("hello", font=("Courier", 90, "normal"), align="center")

    assert turtle.screen.action["text"] == "hello"
    assert turtle.screen.action["font"] == ("Courier", 90, "normal")
    assert turtle.screen.action["align"] == "center"


def test_turtle_circle():
    """
    Check turtle circle.
    """
    turtle = Turtle()
    turtle.circle(120, 180)
    turtle.circle(10)
    turtle.forward(100)
    assert abs(turtle.pos()[0] + 100) < 1e-5
    assert abs(turtle.pos()[1] - 240) < 1e-5
    assert abs(turtle.heading() - 180) < 1e-5


def test_multi_turtles():
    """
    Check multi-turtles.
    """
    s = Screen()

    A = Turtle(s)
    assert A.x == Screen.WIDTH / 2
    assert A.y == Screen.HEIGHT / 2

    B = Turtle(s)
    assert B.x == Screen.WIDTH / 2
    assert B.y == Screen.HEIGHT / 2

    A.forward(80)
    assert A.x == Screen.WIDTH / 2 + 80
    assert A.y == Screen.HEIGHT / 2

    B.right(90)
    B.forward(80)
    assert B.x == Screen.WIDTH / 2
    assert B.y == Screen.HEIGHT / 2 + 80


def test_logo_mode():
    """
    Check logo mode method.
    """
    t = Turtle()
    t.mode("logo")
    assert t.heading() == 0

    t.left(45)
    t.fd(100)
    t.right(90)
    t.fd(100)
    assert t.heading() == 45

    t.setheading(300)
    t.heading() == 300
