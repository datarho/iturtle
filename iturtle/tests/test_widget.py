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

    assert turtle.x == Turtle.WIDTH // 2
    assert turtle.y == Turtle.HEIGHT // 2

    turtle.forward(80)

    assert turtle.x == Turtle.WIDTH // 2 + 80
    assert turtle.y == Turtle.HEIGHT // 2

    turtle.right(90)
    turtle.forward(80)

    assert turtle.x == Turtle.WIDTH // 2 + 80
    assert turtle.y == Turtle.HEIGHT // 2 + 80


def test_turtle_backward():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.x == Turtle.WIDTH // 2
    assert turtle.y == Turtle.HEIGHT // 2

    turtle.backward(80)

    assert turtle.x == Turtle.WIDTH // 2 - 80
    assert turtle.y == Turtle.HEIGHT // 2

    turtle.right(90)
    turtle.backward(80)

    assert turtle.x == Turtle.WIDTH // 2 - 80
    assert turtle.y == Turtle.HEIGHT // 2 - 80


def test_turtle_right():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.bearing == 0

    turtle.right(90)

    assert turtle.bearing == 90

    turtle.right(360)

    assert turtle.bearing == 90


def test_turtle_left():
    """
    Check turtle backward method.
    """
    turtle = Turtle()

    assert turtle.bearing == 0

    turtle.left(90)

    assert turtle.bearing == 270

    turtle.right(360)

    assert turtle.bearing == 270
