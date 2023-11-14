"""
Test cases for turtle creation.
"""

import pytest

from ..turtle import Turtle


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

    assert turtle.x == Turtle.WIDTH / 2
    assert turtle.y == Turtle.HEIGHT / 2

    turtle.forward(80)

    assert turtle.x == Turtle.WIDTH / 2 + 80
    assert turtle.y == Turtle.HEIGHT / 2

    turtle.right(90)
    turtle.forward(80)

    assert turtle.x == Turtle.WIDTH / 2 + 80
    assert turtle.y == Turtle.HEIGHT / 2 + 80


def test_turtle_backward():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.x == Turtle.WIDTH / 2
    assert turtle.y == Turtle.HEIGHT / 2

    turtle.backward(80)

    assert turtle.x == Turtle.WIDTH / 2 - 80
    assert turtle.y == Turtle.HEIGHT / 2

    turtle.right(90)
    turtle.backward(80)

    assert turtle.x == Turtle.WIDTH / 2 - 80
    assert turtle.y == Turtle.HEIGHT / 2 - 80


def test_turtle_right():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.bearing == 0

    turtle.right(90)

    assert turtle.bearing == 90

    turtle.right(360)

    assert turtle.bearing == 450


def test_turtle_left():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.bearing == 0

    turtle.left(90)

    assert turtle.bearing == -90

    turtle.right(360)

    assert turtle.bearing == 270


def test_turtle_goto():
    """
    Check turtle goto method.
    """
    turtle = Turtle()

    turtle.forward(10)
    turtle.goto(0, 0)

    assert turtle.x == Turtle.WIDTH / 2
    assert turtle.y == Turtle.HEIGHT / 2

    turtle = Turtle()

    turtle.forward(10)
    turtle.goto((0, 0))

    assert turtle.x == Turtle.WIDTH / 2
    assert turtle.y == Turtle.HEIGHT / 2


def test_turtle_teleport():
    """
    Check turtle teleport method.
    """
    turtle = Turtle()
    turtle.forward(10)
    turtle.teleport(0, 0)

    assert turtle.x == Turtle.WIDTH / 2
    assert turtle.y == Turtle.HEIGHT / 2


def test_turtle_dot():
    """
    Check turtle dot method.
    """
    turtle = Turtle()

    turtle.dot()

    assert turtle.action["size"] == 5

    turtle.dot(50)

    assert turtle.action["size"] == 50

    turtle.dot(50, "blue")

    assert turtle.action["color"] == "blue"
    assert turtle.action["size"] == 50

    turtle.dot(50, (255, 0, 0))

    assert turtle.action["color"] == (255, 0, 0)
    assert turtle.action["size"] == 50


def test_turtle_towards():
    """
    Check turtle towards, pos and setheading method.
    """
    turtle = Turtle()

    turtle.forward(10)
    turtle.setheading(turtle.towards(0, 0))
    turtle.fd(10)

    assert turtle.x == Turtle.WIDTH / 2
    assert turtle.y == Turtle.HEIGHT / 2
    assert abs(turtle.pos()[0]) < 1e-5
    assert abs(turtle.pos()[1]) < 1e-5

    turtle = Turtle()

    turtle.forward(10)
    turtle.setheading(turtle.towards((0, 0)))
    turtle.fd(10)

    assert turtle.x == Turtle.WIDTH / 2
    assert turtle.y == Turtle.HEIGHT / 2
    assert abs(turtle.pos()[0]) < 1e-5
    assert abs(turtle.pos()[1]) < 1e-5


def test_turtle_write():
    """
    Check turtle write texts.
    """
    turtle = Turtle()

    turtle.write("hello world")

    assert turtle.action["text"] == "hello world"
    assert turtle.action["align"] == "left"
    assert turtle.action["font"] == ("Arial", 8, "normal")

    turtle = Turtle()

    turtle.write("hello world", "right")

    assert turtle.action["text"] == "hello world"
    assert turtle.action["align"] == "right"
    assert turtle.action["font"] == ("Arial", 8, "normal")

    turtle = Turtle()
    turtle.write("hello", font=("Courier", 90, "normal"), align="center")

    assert turtle.action["text"] == "hello"
    assert turtle.action["font"] == ("Courier", 90, "normal")
    assert turtle.action["align"] == "center"
