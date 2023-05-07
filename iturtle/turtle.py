#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Samuel Zhang.
# Distributed under the terms of the Modified BSD License.

"""
Interactive turtle widget module
"""

from enum import StrEnum
from math import cos, radians, sin

from IPython.display import display
from ipywidgets import DOMWidget
from traitlets import List, Int, Unicode

from .frontend import MODULE_NAME, MODULE_VERSION


class ActionType(StrEnum):
    """
    Enum for action types that follows SVG path commands.
    """

    MOVE_ABSOLUTE = "M"
    MOVE_RELATIVE = "m"
    LINE_ABSOLUTE = "L"


class Turtle(DOMWidget):
    """Interactive turtle widget"""

    # Define constants here.
    
    WIDTH = 800
    HEIGHT = 600

    # Jupyter model variables.

    _model_name = Unicode("TurtleModel").tag(sync=True)
    _model_module = Unicode(MODULE_NAME).tag(sync=True)
    _model_module_version = Unicode(MODULE_VERSION).tag(sync=True)
    _view_name = Unicode("TurtleView").tag(sync=True)
    _view_module = Unicode(MODULE_NAME).tag(sync=True)
    _view_module_version = Unicode(MODULE_VERSION).tag(sync=True)

    # Widget state goes here.

    width = Int(WIDTH).tag(sync=True)
    height = Int(HEIGHT).tag(sync=True)
    x = Int(WIDTH // 2).tag(sync=True)
    y = Int(HEIGHT // 2).tag(sync=True)
    actions = List().tag(sync=True)
    bearing = Int(0).tag(sync=True)

    def __init__(self):
        """Create a Turtle.
        Example:
            t = Turtle()
        """
        super(Turtle, self).__init__()

        self.pen = True
        self.speedVar = 1
        self.color = "black"

        self.actions = []

        self.home()

        # The client should call display proactively.

        # display(self)

    def home(self):
        """
        Move the Turtle to its home position.
        Example:
            t.home()
        """
        self.x = self.width // 2
        self.y = self.height // 2
        self.bearing = 0
        self._add_action(ActionType.MOVE_ABSOLUTE)

    def penup(self):
        """
        Lift up the pen.
        Example:
            t.penup()
        """
        self.pen = False

    def pendown(self):
        """
        Put down the pen. Turtles start with their pen down.
        Example:
            t.pendown()
        """
        self.pen = True

    def speed(self, speed):
        """
        Change the speed of the turtle (range 1-10) where 1 is slowest and 10 is fastest.
        Example:
            t.speed(10) # Full speed
        """
        self.speedVar = min(max(1, speed), 10)

    def forward(self, units: int):
        """
        Move the Turtle forward by certain units.
        Example:
            t.forward(100)
        """
        alpha = radians(self.bearing)
        self.x += round(units * cos(alpha))
        self.y += round(units * sin(alpha))

        if self.pen:
            self._add_action(ActionType.LINE_ABSOLUTE)
        else:
            self._add_action(ActionType.MOVE_ABSOLUTE)

    def right(self, num):
        """
        Turn the turtle num degrees to the right.
        Example:
            t.right(90)
        """
        self.bearing = (self.bearing + num) % 360

    def left(self, num):
        """Turn the Turtle num degrees to the left.
        Example::
            t.left(90)
        """
        self.bearing = (self.bearing - num) % 360

    def _add_action(self, action_type: ActionType):
        action = dict(
            type=action_type,
            pen=self.pen,
            color=self.color,
            position=(self.x, self.y),
            speed=self.speedVar,
        )
        self.actions = self.actions + [action]
