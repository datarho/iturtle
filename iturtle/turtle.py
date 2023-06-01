#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Samuel Zhang.
# Distributed under the terms of the Modified BSD License.

"""
Interactive turtle widget module
"""

from enum import Enum
from math import cos, radians, sin
from time import sleep
from typing import overload

from IPython.display import clear_output, display
from ipywidgets import DOMWidget
from svg import SVG, Circle, Line, Rect, ViewBoxSpec
from traitlets import Int, List, Unicode

from .frontend import MODULE_NAME, MODULE_VERSION


class ActionType(str, Enum):
    """
    Enum for action types that follows SVG path commands.
    """

    MOVE_ABSOLUTE = "M"
    MOVE_RELATIVE = "m"
    LINE_ABSOLUTE = "L"


class Turtle(DOMWidget):
    """
    Interactive turtle widget
    """

    # Define constants here.

    WIDTH = 800
    HEIGHT = 500

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
    distance = Int(0).tag(sync=True)
    velocity = Int(6).tag(sync=True)  # avoid duplicate to speed method
    background = Unicode("white").tag(sync=True)

    def __init__(self):
        """Create a Turtle.
        Example:
            t = Turtle()
        """
        super(Turtle, self).__init__()

        display(self)

        self.pen = True
        self.velocity = 6
        self.pen_color = "black"

        self.actions = []

        self.home()

    def home(self):
        """
        Move the Turtle to its home position.
        Example:
            t.home()
        """
        self.x = self.width // 2
        self.y = self.height // 2
        self.distance = 0
        self.bearing = 0
        self._add_action(ActionType.MOVE_ABSOLUTE)

    def clear(self):
        """
        This function is used to delete the turtle’s drawings from the screen. Do not move state
        and position of the turtle as well as drawings of other turtles are not affected.
        Example:
            t.clear()
        """
        self.actions = []

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

    def speed(self, velocity: int):
        """
        Change the speed of the turtle (range 1-10) where 1 is slowest and 10 is fastest.
        Example:
            t.speed(10) # Full speed
        """
        self.velocity = self._clamp(velocity, 1, 10)

    def forward(self, distance: int):
        """
        Move the Turtle forward by certain units.
        Example:
            t.forward(100)
        """
        self.distance = distance

        alpha = radians(self.bearing)
        self.x += round(distance * cos(alpha))
        self.y += round(distance * sin(alpha))

        if self.pen:
            self._add_action(ActionType.LINE_ABSOLUTE)
        else:
            self._add_action(ActionType.MOVE_ABSOLUTE)

    def right(self, angle: int):
        """
        Turn the turtle num degrees to the right.
        Example:
            t.right(90)
        """
        self.bearing = (self.bearing + angle) % 360

    def left(self, angle: int):
        """Turn the Turtle num degrees to the left.
        Example::
            t.left(90)
        """
        self.bearing = (self.bearing - angle) % 360

    @overload
    def pencolor(self, color: str) -> None:
        ...

    @overload
    def pencolor(self, r: int, g: int, b: int) -> None:
        ...

    def pencolor(self, *args) -> None:
        """
        Change the color of the pen with RGB color. Default is black.
        Example:
            t.pencolor("red")
        """
        if len(args) == 3:
            r = self._clamp(args[0], 0, 255)
            g = self._clamp(args[1], 0, 255)
            b = self._clamp(args[2], 0, 255)

            self.pen_color = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        elif len(args) == 1:
            self.pen_color = args[0]

    def heading(self) -> int:
        """
        Return the turtle's current heading.
        """
        return self.bearing

    @overload
    def bgcolor(self, color: str) -> None:
        ...

    @overload
    def bgcolor(self, r: int, g: int, b: int) -> None:
        ...

    def bgcolor(self, *args) -> None:
        """
        Set or return background color of the turtle screen.
        Example:
            t.bgcolor("orange")
        """
        if len(args) == 3:
            r = self._clamp(args[0], 0, 255)
            g = self._clamp(args[1], 0, 255)
            b = self._clamp(args[2], 0, 255)

            self.background = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        elif len(args) == 1:
            self.background = args[0]

    def save(self) -> None:
        clear_output()
        display(self)

    def _clamp(self, num: int, low: int, high: int) -> int:
        return max(low, min(num, high))

    def _add_action(self, action_type: ActionType):
        action = dict(
            type=action_type,
            pen=self.pen,
            color=self.pen_color,
            distance=self.distance,
            position=(self.x, self.y),
            velocity=self.velocity,
        )
        self.actions = self.actions + [action]
        if action_type in [ActionType.LINE_ABSOLUTE]:
            self._run()

    def _run(self):
        # By default the motion of a turtle is broken up into a number of individual steps determined by:
        #   steps = int(distance / (3 * 1.1**speed * speed))
        # At the default speed (3 or 'slow'), a 100px line would be drawn in 8 steps. At the slowest speed
        # (1 or 'slowest'), 30 steps. At a fast speed (10 or 'fast'), 1 step. Oddly, the default speed isn't
        # the 'normal' (6) speed! Each step incurs a screen update delay of 10ms by default.
        steps = int(self.distance / (3 * 1.1**self.velocity * self.velocity))
        sleep(steps * 0.01)

    def _repr_svg_(self):
        position = [0, 0]
        lines = []

        for action in self.actions:
            if action["type"] == ActionType.MOVE_ABSOLUTE:
                position = action["position"]
            elif action["type"] == ActionType.LINE_ABSOLUTE:
                line = Line(x1=position[0], y1=position[1], x2=action["position"][0], y2=action["position"][1], stroke=action["color"])
                lines.append(line)
                position = action["position"]

        pic = SVG(
            width=self.width,
            height=self.height,
            viewBox=ViewBoxSpec(0, 0, self.width + 1, self.height + 1),
            elements=[
                Rect(width=self.width, height=self.height, fill=self.background), 
            ] + lines,
        )

        return str(pic)
