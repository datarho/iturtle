from math import atan2, cos, degrees, radians, sin, sqrt
from typing import Optional, Tuple, overload

from .screen import ActionType, Screen
from time import sleep

class Turtle:
    MODE = "standard"

    def __init__(self, screen: Optional[Screen] = None):
        if screen is None:
            self.screen = Screen()
        else:
            self.screen = screen
        self.id = id(self)

        self.x = self.screen.WIDTH / 2
        self.y = self.screen.HEIGHT / 2
        self.bearing = 0
        if Turtle.MODE == "logo":
            self.bearing = 90
        self.show = True
        self.pen = True
        self.pen_color = "black"
        self.pen_size = 1
        self._distance = 0
        self.radius = 0
        self.clockwise = 1
        self.media = None
        self.turtleShape = ""

        # Text related variable.

        self.text = ""
        self.font = ("Arial", 8, "normal")
        self.align = "left"

        self._update_state()

        self.penup()
        self.home()
        self.pendown()

    def _update_state(self):
        """
        Update turtle state in the screen.

        Here we convert object id to string to be compliant with JSON spec.
        """
        self.screen.turtles = {
            **self.screen.turtles,
            str(self.id): {
                "x": self.x,
                "y": self.y,
                "bearing": self.bearing,
                "show": self.show,
                "shape": self.turtleShape
            },
        }

    def pos(self):
        return (self.x - self.screen.width / 2, self.screen.height / 2 - self.y)

    def set_turtle_pos(self, x: float, y: float):
        self.x, self.y = (x + self.screen.width / 2, self.screen.height / 2 - y)
        self._update_state()

    def home(self):
        """
        Move the Turtle to its home position.

        Example:
        >>> turtle.home()
        """
        self.set_turtle_pos(0, 0)
        self._distance = 0
        self.bearing = 0
        if self.pen:
            self.screen._add_action(self, ActionType.LINE_ABSOLUTE)
        else:
            self.screen._add_action(self, ActionType.MOVE_ABSOLUTE)
        self._update_state()

    def clear(self):
        """
        This function is used to delete the turtle’s drawings from the screen. Do not move state
        and position of the turtle as well as drawings of other turtles are not affected.

        Example:
        >>> turtle.clear()
        """
        self.screen._add_action(self, ActionType.CLEAR)

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

    def speed(self, velocity=None):
        """
        Change the speed of the turtle (range 1-10) where 1 is slowest and 10 is fastest, 0 is fastest too.
        'fastest' :  0
        'fast'    :  10
        'normal'  :  6
        'slow'    :  3
        'slowest' :  1
        Example:
        >>> turtle.speed(10) # Full speed
        """
        if velocity is None:
            return self.screen.velocity
        if type(velocity) is str:
            if velocity == "fastest":
                self.screen.velocity = 10
            elif velocity == "fast":
                self.screen.velocity = 10
            elif velocity == "normal":
                self.screen.velocity = 6
            elif velocity == "slow":
                self.screen.velocity = 3
            elif velocity == "slowest":
                self.screen.velocity = 1
        else:
            if velocity == 0:
                velocity = 10
            self.screen.velocity = self._clamp(velocity, 1, 10)
        return self.screen.velocity

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
        self._distance = distance

        alpha = radians(self.bearing)
        ix, iy = self.pos()
        self.set_turtle_pos(ix + distance * cos(alpha), iy + distance * sin(alpha))
        if self.pen:
            self.screen._add_action(self, ActionType.LINE_ABSOLUTE)
        else:
            self.screen._add_action(self, ActionType.MOVE_ABSOLUTE)

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
    def goto(self, x: Tuple[float, float]) -> None: ...

    @overload
    def goto(self, x: float, y: float) -> None: ...

    def goto(self, *coordinates) -> None:
        """Move the Turtle to the (x, y).

        Example:
        >>> turtle.goto(0, 0)
        """
        if len(coordinates) == 1:
            x, y = coordinates[0]
        else:
            x, y = coordinates
        self._distance = self.distance(x, y)
        self.set_turtle_pos(x, y)
        if self.pen:
            self.screen._add_action(self, ActionType.LINE_ABSOLUTE)
        else:
            self.screen._add_action(self, ActionType.MOVE_ABSOLUTE)

    def teleport(self, x: float, y: float):
        """Teleport the Turtle to (x,y).

        Example:
        >>> turtle.teleport(0, 0)
        """
        self.set_turtle_pos(x, y)
        self._distance = 0
        self.screen._add_action(self, ActionType.MOVE_ABSOLUTE)

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
        self.bearing = self.bearing - angle
        self._update_state()
        sleep(0.05)

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
        self.bearing = self.bearing + angle
        self._update_state()
        sleep(0.05)

    @overload
    def dot(self) -> None: ...

    @overload
    def dot(self, size: int, color: str) -> None: ...

    @overload
    def dot(self, size: int, color: Tuple[int, int, int]) -> None: ...

    def dot(self, size: Optional[int] = None, *color) -> None:
        """Draw a circular dot with diameter size, using color.

        Example:
        >>> turtle.dot()
        >>> turtle.dot(20, "blue")
        >>> turtle.dot(20, (254, 235, 105))
        """
        self._distance = 0

        tmp_color = self.pen_color
        if size is None:
            self.radius = max((self.pen_size + 4) / 2, self.pen_size)
        else:
            self.radius = size / 2
        if len(color) == 3:
            r = self._clamp(color[0], 0, 255)
            g = self._clamp(color[1], 0, 255)
            b = self._clamp(color[2], 0, 255)
            self.pen_color = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        elif len(color) == 1:
            if type(color[0]) is str:
                self.pen_color = color[0]
            else:
                self.pen_color = "#{0:02x}{1:02x}{2:02x}".format(*color[0])

        self.screen._add_action(self, ActionType.DRAW_DOT)
        self.pen_color = tmp_color

    @overload
    def pencolor(self, color: str) -> None: ...

    @overload
    def pencolor(self, r: int, g: int, b: int) -> None: ...

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
            if type(color[0]) is str:
                self.pen_color = color[0]
            else:
                self.pen_color = "#{0:02x}{1:02x}{2:02x}".format(*color[0])

    def heading(self) -> float:
        """
        Return the turtle's current heading.
        """
        self.bearing = (self.bearing % 360 + 360) % 360
        if Turtle.MODE == "logo":
            return ((90 - self.bearing) % 360 + 360) % 360
        else:
            return self.bearing

    def setheading(self, bearing: float):
        """
        Set the turtle's current heading.
        """
        if Turtle.MODE == "logo":
            self.bearing = ((90 - bearing) % 360 + 360) % 360
        else:
            self.bearing = (bearing % 360 + 360) % 360
        self._update_state()

    def __circle(self, radius: float, extent: float):
        ix, iy = self.pos()
        if radius > 0:
            alpha = radians(-self.bearing - 90)
            extent = -abs(extent)
            self.clockwise = 0
        else:
            alpha = radians(-self.bearing + 90)
            extent = +abs(extent)
            self.clockwise = 1
        self.bearing = self.bearing - extent

        self.radius = abs(radius)
        dx, dy = ix + self.radius * cos(alpha), iy - self.radius * sin(alpha)
        alpha = alpha - radians(180) + radians(extent)
        dx, dy = dx + self.radius * cos(alpha), dy - self.radius * sin(alpha)
        self.set_turtle_pos(dx, dy)
        self._distance = self.radius * radians(abs(extent))
        self.screen._add_action(self, ActionType.CIRCLE)

    def circle(self, radius: float, extent=None):
        if extent is None:
            extent = 360
        while extent >= 180:
            self.__circle(radius, 180)
            extent -= 180
        if extent > 0:
            self.__circle(radius, extent)

    @overload
    def towards(self, x: Tuple[float, float]) -> None: ...

    @overload
    def towards(self, x: float, y: float) -> None: ...

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
        return degrees(atan2(dy, dx))

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
        self._update_state()

        sleep(0.1)

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
        self._update_state()

    @overload
    def bgcolor(self, color: str) -> None: ...

    @overload
    def bgcolor(self, r: int, g: int, b: int) -> None: ...

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

            self.screen.background = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        elif len(args) == 1:
            self.screen.background = args[0]

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
        self._distance = 0
        self.screen._add_action(self, ActionType.WRITE_TEXT)
        self.text = None

    def play(self, sound) -> None:
        """
        Play sound effect which could be mp3 or ogg file.

        Arguments:
        * sound -- the url of the sound file
        """
        self.media = sound
        self._distance = 0
        self.screen._add_action(self, ActionType.SOUND)
        self.media = None

    def save(self) -> None:
        self.screen.save()

    def _clamp(self, num: int, low: int, high: int) -> int:
        return max(low, min(num, high))

    def pensize(self, width: Optional[int] = None):
        if width is None:
            self.pen_size = 1
        else:
            self.pen_size = width

    def distance(self, x: float, y: float) -> float:
        ix, iy = self.pos()
        return sqrt((ix - x) ** 2 + (iy - y) ** 2)

    def mode(self, mode: Optional[str] = None) -> str:
        if mode is None:
            return Turtle.MODE
        elif mode == "logo":
            self.bearing = 90
            Turtle.MODE = mode
        elif mode == "standard":
            self.bearing = 0
            Turtle.MODE = mode
        self._update_state()
        return Turtle.MODE

    def shape(self, src: str= ""):
        self.turtleShape = src
        self._update_state()
