#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Samuel Zhang.
# Distributed under the terms of the Modified BSD License.

"""
Interactive turtle widget module
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, List
from .frontend import MODULE_NAME, MODULE_VERSION
from IPython.display import display


class Turtle(DOMWidget):
    """Interactive turtle widget"""

    _model_name = Unicode("TurtleModel").tag(sync=True)
    _model_module = Unicode(MODULE_NAME).tag(sync=True)
    _model_module_version = Unicode(MODULE_VERSION).tag(sync=True)
    _view_name = Unicode("TurtleView").tag(sync=True)
    _view_module = Unicode(MODULE_NAME).tag(sync=True)
    _view_module_version = Unicode(MODULE_VERSION).tag(sync=True)

    # Your widget state goes here. Make sure to update the corresponding

    points = List(sync=True)

    SIZE = 400
    OFFSET = 20

    def __init__(self):
        """Create a Turtle.
        Example::
            t = Turtle()
        """
        super(Turtle, self).__init__()

        display(self)

        self.pen = 1
        self.speedVar = 1
        self.color = "black"
        self.bearing = 90
        self.points = []

        self.home()

    def home(self):
        """
        Move the Turtle to its home position.
        Example::
            t.home()
        """
        self.posX = 200
        self.posY = 200
        if 90 < self.bearing <= 270:
            self.b_change = -(self.bearing - 90)
        else:
            self.b_change = 90 - self.bearing
        self.bearing = 90
        self._add_point()

    def penup(self):
        """
        Lift up the pen.
        Example:
            t.penup()
        """
        self.pen = 0

    def speed(self, speed):
        """
        Change the speed of the turtle (range 1-10).
        Example::
            t.speed(10) # Full speed
        """
        self.speedVar = min(max(1, speed), 10)

    def _add_point(self):
        point = dict(
            pen=self.pen,
            color=self.color,
            pos_x=self.posX,
            pos_y=self.posY,
            change=self.b_change,
            speed=self.speedVar,
        )
        self.points = self.points + [point]
