"""
Interactive turtle widget module
"""
from enum import Enum
from math import atan2, cos, degrees, radians, sin, sqrt
from time import sleep
from typing import Tuple, overload

from IPython.display import clear_output, display
from ipywidgets import DOMWidget
from traitlets import Bool, Dict, Float, Int, Unicode

from .frontend import MODULE_NAME, MODULE_VERSION


class ActionType(str, Enum):
    """
    Enum for action types that follows SVG path commands.
    """

    MOVE_ABSOLUTE = "M"
    MOVE_RELATIVE = "m"
    LINE_ABSOLUTE = "L"
    DRAW_DOT = "D"
    WRITE_TEXT = "W"


class Turtle(DOMWidget):
    """
    Interactive turtle widget
    """

    # Define constants here.

    WIDTH = 800
    HEIGHT = 500
    PENSIZE = 1
    DELAY = 2

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
    x = Float(WIDTH / 2).tag(sync=True)
    y = Float(HEIGHT / 2).tag(sync=True)
    id = Int(0).tag(sync=True)
    bearing = Float(0).tag(sync=True)
    distance = Float(0).tag(sync=True)
    velocity = Int(3).tag(sync=True)  # avoid duplicate to speed method
    background = Unicode("white").tag(sync=True)
    show = Bool(True).tag(sync=True)

    # We will only sync delta action so that frontend will handle the whole states.

    action = Dict().tag(sync=True)

    def __init__(self):
        """
        Create a Turtle.

        Example:
        >>> t = Turtle()
        """
        super(Turtle, self).__init__()

        display(self)

        # Move related variables.

        self.pen = True
        self.pen_color = "black"
        self.pen_size = self.PENSIZE
        self.velocity = 6
        self.id = id(self)
        self.action = {}

        # Text related variable.

        self.text = ""
        self.font = ("Arial", 8, "normal")
        self.align = "left"

        self.penup()
        self.home()
        self.pendown()

    def pos(self):
        return (self.x - self.width / 2, self.height / 2 - self.y)

    def set_turtle_pos(self, x: float, y: float):
        self.x, self.y = (x + self.width / 2, self.height / 2 - y)

    def home(self):
        """
        Move the Turtle to its home position.

        Example:
        >>> turtle.home()
        """
        self.set_turtle_pos(0, 0)
        self.distance = 0
        self.bearing = 0
        if self.pen:
            self._add_action(ActionType.LINE_ABSOLUTE)
        else:
            self._add_action(ActionType.MOVE_ABSOLUTE)

    def clear(self):
        """
        This function is used to delete the turtle’s drawings from the screen. Do not move state
        and position of the turtle as well as drawings of other turtles are not affected.

        Example:
        >>> turtle.clear()
        """
        self.action = {}

    def pu(self):
        """
        Lift up the pen.

        Example:
        >>> turtle.pu()
        """
        self.penup()

    def penup(self):
        """
        Lift up the pen.

        Example:
        >>> turtle.penup()
        """
        self.pen = False

    def pd(self):
        """
        Put down the pen. Turtles start with their pen down.

        Example:
        >>> turtle.pd()
        """
        self.pendown()

    def pendown(self):
        """
        Put down the pen. Turtles start with their pen down.

        Example:
        >>> turtle.pendown()
        """
        self.pen = True

    def speed(self, velocity: int):
        """
        Change the speed of the turtle (range 1-10) where 1 is slowest and 10 is fastest.

        Example:
        >>> turtle.speed(10) # Full speed
        """
        self.velocity = self._clamp(velocity, 1, 10)

    def fd(self, distance: float):
        """
        Move the Turtle forward by certain units.

        Example:
        >>> turtle.fd(100)
        """
        self.forward(distance)

    def forward(self, distance: float):
        """
        Move the Turtle forward by certain units.

        Example:
        >>> turtle.forward(100)
        """
        self.distance = distance

        alpha = radians(self.bearing)
        x, y = self.pos()
        self.set_turtle_pos(x + distance * cos(alpha), y - distance * sin(alpha))
        if self.pen:
            self._add_action(ActionType.LINE_ABSOLUTE)
        else:
            self._add_action(ActionType.MOVE_ABSOLUTE)

    def bk(self, distance: float):
        """
        Move the Turtle backward by certain units.

        Example:
        >>> turtle.bk(100)
        """
        self.backward(distance)

    def backward(self, distance: float):
        """
        Move the Turtle backward by certain units.

        Example:
        >>> turtle.backward(100)
        """
        self.forward(-distance)

    @overload
    def goto(self, x: Tuple[float, float]) -> None:
        ...

    @overload
    def goto(self, x: float, y: float) -> None:
        ...

    def goto(self, *coordinates) -> None:
        """Move the Turtle to the (x, y).

        Example:
        >>> turtle.goto(0, 0)
        """
        if len(coordinates) == 1:
            x, y = coordinates[0]
        else:
            x, y = coordinates
        self.distance = sqrt((self.pos()[0] - x) ** 2 + (self.pos()[1] - y) ** 2)
        self.set_turtle_pos(x, y)
        if self.pen:
            self._add_action(ActionType.LINE_ABSOLUTE)
        else:
            self._add_action(ActionType.MOVE_ABSOLUTE)

    def teleport(self, x: float, y: float):
        """Teleport the Turtle to (x,y).

        Example:
        >>> turtle.teleport(0, 0)
        """
        self.set_turtle_pos(x, y)
        self.distance = 0
        self._add_action(ActionType.MOVE_ABSOLUTE)

    def rt(self, angle: float):
        """
        Turn the turtle num degrees to the right.

        Example:
        >>> turtle.rt(90)
        """
        self.right(angle)

    def right(self, angle: float):
        """
        Turn the turtle num degrees to the right.

        Example:
        >>> turtle.right(90)
        """
        self.bearing = self.bearing + angle

    def lt(self, angle: float):
        """Turn the Turtle num degrees to the left.

        Example:
        >>> turtle.lt(90)
        """
        self.left(angle)

    def left(self, angle: int):
        """Turn the Turtle num degrees to the left.

        Example:
        >>> turtle.left(90)
        """
        self.bearing = self.bearing - angle

    @overload
    def dot(self) -> None:
        ...

    @overload
    def dot(self, size: int, color: str) -> None:
        ...

    @overload
    def dot(self, size: int, color: Tuple[int, int, int]) -> None:
        ...

    def dot(self, size: int = None, *color) -> None:
        """Draw a circular dot with diameter size, using color.

        Example:
        >>> turtle.dot()
        >>> turtle.dot(20, "blue")
        >>> turtle.dot(20, (254, 235, 105))
        """
        self.distance = 0

        tmp_color = self.pen_color
        tmp_size = self.pen_size
        if size is None:
            self.pen_size = max(self.PENSIZE + 4, 2 * self.PENSIZE)
        else:
            self.pen_size = size
        if len(color) == 3:
            r = self._clamp(color[0], 0, 255)
            g = self._clamp(color[1], 0, 255)
            b = self._clamp(color[2], 0, 255)
            self.pen_color = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        elif len(color) == 1:
            self.pen_color = color[0]

        self._add_action(ActionType.DRAW_DOT)
        self.pen_color = tmp_color
        self.pen_size = tmp_size

    @overload
    def pencolor(self, color: str) -> None:
        ...

    @overload
    def pencolor(self, r: int, g: int, b: int) -> None:
        ...

    def pencolor(self, *color) -> None:
        """
        Change the color of the pen with RGB color. Default is black.

        Example:
        >>> turtle.pencolor("red")
        """
        if len(color) == 3:
            r = self._clamp(color[0], 0, 255)
            g = self._clamp(color[1], 0, 255)
            b = self._clamp(color[2], 0, 255)

            self.pen_color = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        elif len(color) == 1:
            self.pen_color = color[0]

    def heading(self) -> float:
        """
        Return the turtle's current heading.
        """
        return self.bearing

    def setheading(self, bearing: float):
        """
        Set the turtle's current heading.
        """
        self.bearing = bearing

    @overload
    def towards(self, x: Tuple[float, float]) -> None:
        ...

    @overload
    def towards(self, x: float, y: float) -> None:
        ...

    def towards(self, *coordinates) -> None:
        """
        Return the angle between the line from turtle position to position specified by (x,y), the vector
        or the other turtle.

        Example:
        >>> turtle.towards(0,0)
        """
        if len(coordinates) == 1:
            x, y = coordinates[0]
        else:
            x, y = coordinates

        ix, iy = self.pos()
        dx = x - ix
        dy = y - iy
        if dx or dy:
            return degrees(atan2(dx, dy)) - 90
        else:
            return self.bearing

    def ht(self):
        """
        Make the turtle invisible. It’s a good idea to do this while you’re in the middle of doing some
        complex drawing, because hiding the turtle speeds up the drawing observably.

        Example:
        >>> turtle.hideturtle()
        """
        self.hideturtle()

    def hideturtle(self):
        """
        Make the turtle invisible. It’s a good idea to do this while you’re in the middle of doing some
        complex drawing, because hiding the turtle speeds up the drawing observably.

        Example:
        >>> turtle.hideturtle()
        """
        self.show = False

    def st(self):
        """
        Make the turtle visible.
        Example:
        >>> turtle.st()
        """
        self.showturtle()

    def showturtle(self):
        """
        Make the turtle visible.

        Example:
        >>> turtle.showturtle()
        """
        self.show = True

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
        >>> turtle.bgcolor("orange")
        """
        if len(args) == 3:
            r = self._clamp(args[0], 0, 255)
            g = self._clamp(args[1], 0, 255)
            b = self._clamp(args[2], 0, 255)

            self.background = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        elif len(args) == 1:
            self.background = args[0]

    def write(
        self,
        arg,
        align: str = "left",
        font: Tuple[str, int, str] = ("Arial", 8, "normal"),
    ) -> None:
        """
        Write text at the current turtle position.

        Arguments:
        * arg -- info, which is to be written to the screen
        * align (optional) -- one of the strings "left", "center" or right"
        * font (optional) -- a triple (name, size, type)

        Write text - the string representation of arg - at the current
        turtle position according to align ("left", "center" or right")
        and with the given font.

        Example (for a Turtle instance named turtle):
        >>> turtle.write('Home = ', align="center")
        >>> turtle.write((0,0))
        """
        self.text = str(arg)
        self.align = align.lower()
        self.font = font
        self._add_action(ActionType.WRITE_TEXT)
        self.text = None

    def save(self) -> None:
        clear_output()
        display(self)

    def _clamp(self, num: int, low: int, high: int) -> int:
        return max(low, min(num, high))

    def _add_action(self, action_type: ActionType):
        # Build basic action properties

        action = dict(
            type=action_type,
            pen=self.pen,
            color=self.pen_color,
            distance=self.distance,
            position=(self.x, self.y),
            velocity=self.velocity,
            size=self.pen_size,
        )

        # Build optional action properties.

        if self.text:
            action["text"] = self.text
            action["font"] = self.font
            action["align"] = self.align

        # Swap to instance action variable for sync.

        self.action = action

        self._run()

    def _run(self):
        # By default the motion of a turtle is broken up into a number of individual steps determined by:
        #   steps = int(distance / (3 * 1.1**speed * speed))
        # At the default speed (3 or 'slow'), a 100px line would be drawn in 8 steps. At the slowest speed
        # (1 or 'slowest'), 30 steps. At a fast speed (10 or 'fast'), 1 step.

        steps = max(
            abs(self.distance)
            * self.DELAY
            / (3 * 1.1**self.velocity * self.velocity),
            1,
        )

        # Each step incurs a screen update delay of 100ms by default. We should not shorten the delay as
        # websocket won't be able to process all the messages in a short time.

        sleep(steps * 0.05)
