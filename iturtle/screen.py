"""
Interactive turtle widget module
"""

from enum import Enum

from time import sleep

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
    CIRCLE = "C"
    SOUND = "S"
    CLEAR = "CLR"


class Screen(DOMWidget):
    """
    Interactive turtle widget
    """

    # Define constants here.

    WIDTH = 800
    HEIGHT = 500
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
    bgUrl = Unicode("").tag(sync=True)
    background = Unicode("white").tag(sync=True)
    id = Int(0).tag(sync=True)

    bearing = Float(0).tag(sync=True)
    show = Bool(True).tag(sync=True)

    turtles = Dict().tag(sync=True)

    # We will only sync delta action so that frontend will handle the whole states.

    action = Dict().tag(sync=True)

    def __init__(self):
        """
        Create a Screen.

        Example:
        >>> t = Screen()
        """
        super(Screen, self).__init__()

        display(self)
        self.id = id(self)
        self.velocity = 3  # avoid duplicate to speed method

        self.turtles = dict()

    def save(self) -> None:
        clear_output()
        display(self)

    def _add_action(self, turtle, action_type: ActionType):
        # Build basic action properties
        action = dict(
            id=str(turtle.id),
            type=action_type,
            media=turtle.media,
            pen=turtle.pen,
            color=turtle.pen_color,
            distance=abs(turtle._distance),
            position=(turtle.x, turtle.y),
            velocity=self.velocity,
            radius=turtle.radius,
            clockwise=turtle.clockwise,
            size=turtle.pen_size,
        )

        # Build optional action properties.

        if turtle.text:
            action["text"] = turtle.text
            action["font"] = turtle.font
            action["align"] = turtle.align

        # Swap to instance action variable for sync.
        self.action = action

        self._run(turtle._distance)

    def _run(self, distance):
        # By default the motion of a turtle is broken up into a number of individual steps determined by:
        #   steps = int(distance / (3 * 1.1**speed * speed))
        # At the default speed (3 or 'slow'), a 100px line would be drawn in 8 steps. At the slowest speed
        # (1 or 'slowest'), 30 steps. At a fast speed (10 or 'fast'), 1 step.

        steps = max(
            abs(distance) * self.DELAY / (3 * 1.1**self.velocity * self.velocity), 1
        )
        # Each step incurs a screen update delay of 100ms by default. We should not shorten the delay as
        # websocket won't be able to process all the messages in a short time.
        sleep(steps * 0.05)

    def delay(self, d: int) -> None:
        Screen.DELAY = d

    def bgpic(self, src: str):
        self.bgUrl = src