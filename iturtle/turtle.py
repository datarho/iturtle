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

    _model_name = Unicode("TurtleModel").tag(sync=True)
    _model_module = Unicode(MODULE_NAME).tag(sync=True)
    _model_module_version = Unicode(MODULE_VERSION).tag(sync=True)
    _view_name = Unicode("TurtleView").tag(sync=True)
    _view_module = Unicode(MODULE_NAME).tag(sync=True)
    _view_module_version = Unicode(MODULE_VERSION).tag(sync=True)

    # Your widget state goes here. Make sure to update the corresponding
    width = Int(800).tag(sync=True)
    height = Int(500).tag(sync=True)
    x = Int(200).tag(sync=True)
    y = Int(200).tag(sync=True)
    actions = List(sync=True)

    OFFSET = 20

    def __init__(self):
        """Create a Turtle.
        Example:
            t = Turtle()
        """
        super(Turtle, self).__init__()

        display(self)

        self.position = (200, 200)

        self.pen = True
        self.speedVar = 1
        self.change = False
        self.color = "black"
        self.bearing = 90
        self.actions = []

        self.home()

    def home(self):
        """
        Move the Turtle to its home position.
        Example:
            t.home()
        """
        self.position = (200, 200)
        if 90 < self.bearing <= 270:
            self.change = -(self.bearing - 90)
        else:
            self.change = 90 - self.bearing
        self.bearing = 90
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
        Change the speed of the turtle (range 1-10).
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
        if self.pen:
            alpha = radians(self.bearing)
            self.position = (
                self.position[0] + round(units * sin(alpha)),
                self.position[1] + round(units * cos(alpha)),
            )

        self._add_action(ActionType.LINE_ABSOLUTE)

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
            position=self.position,
            speed=self.speedVar,
        )
        self.actions = self.actions + [action]
