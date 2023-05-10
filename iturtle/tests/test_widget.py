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
