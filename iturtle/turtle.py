import uuid

from .screen import ActionType, Screen
from enum import Enum
from math import atan2, cos, degrees, radians, sin, sqrt

class Mode(str, Enum):
  STANDARD = 'standard'
  LOGO = 'logo'
  
class Turtle:
  MODE = Mode.STANDARD
  
  def __init__(self, screen=None):
    if screen:
      self.screen = screen
    else:
      self.screen = Screen()
      
    self.id = str(uuid.uuid4())
    self.x = self.screen.width / 2
    self.y = self.screen.height / 2
    self.speed = 0
    self.bearing = 90 if Turtle.MODE == Mode.LOGO else 0
    self.show = True
    self.pen = True
    self.pencolor = 'black'
    self.pensize = 1
    self.distance = 0
    self.radius = 0
    self.clockwise = 1
    self.media = None
    self.shape = ''
    
    self.text = ""
    self.font = ("Arial", 8, "normal")
    self.align = "left"

    self._add_state()

    self.penup()
    self.home()
    self.pendown()
    
  def _add_state(self):
    self.screen.add_action({
      'id': self.id,
      'type': ActionType.UPDATE_STATE,
      'x': self.x,
      'y': self.y,
      'bearing': self.bearing,
      "show": self.show,
      'shape': self.shape
    })
    
  def _add_action(self, action_type):
    action = {
      'id': self.id,
      'type': action_type,
      'speed': self.speed,
      'media': self.media,
      'pen': self.pen,
      'pencolor': self.pencolor,
      'pensize': self.pensize,
      'distance': abs(self.distance),
      'position': (self.x, self.y),
      'radius': self.radius,
      'clockwise': self.clockwise
    }
    
    if self.text:
      action['text'] = self.text
      action["font"] = self.font
      action["align"] = self.align    
      
    self.screen.add_action(action)
    
  def pos(self, x=None, y=None): # Transfer to screen coordinate
    x = x if x else self.x
    y = y if y else self.y
    
    return (x - self.screen.width / 2, self.screen.height / 2 - y)

  def to_abs_pos(self, x, y):
      return (x + self.screen.width / 2, self.screen.height / 2 - y)
  
  def set_turtle_pos(self, x: float, y: float): # Transfer the screen coordinate to absolute one
    self.x, self.y = self.to_abs_pos(x, y)
    
  def home(self):
    self.distance = 0
    self.bearing = 0
    self.set_turtle_pos(0, 0)
    
    self._add_state()
    self._add_action(ActionType.LINE_ABSOLUTE if self.pen else ActionType.MOVE_ABSOLUTE)
    
  def clear(self):
    self._add_action(ActionType.CLEAR)
    
  def penup(self):
    self.pen = False
  
  def pu(self):
    self.penup()
    
  def pendown(self):
    self.pen = True
    
  def pd(self):
    self.pendown()
    
  # TODO: speed
  
  def forward(self, distance):
    alpha = radians(self.bearing)
    _x, _y = self.pos()
    self.distance = distance
    self.set_turtle_pos(_x  + self.distance * cos(alpha), _y + self.distance * sin(alpha))
    
    self._add_state()
    self._add_action(ActionType.LINE_ABSOLUTE if self.pen else ActionType.MOVE_ABSOLUTE)
    
  def backward(self, distance):
    self.forward(-distance)
    
  def bk(self, distance):
    self.backward(distance)
  
  def goto(self, x, y):
    _x, _y = self.pos()
    self.distance = self._distance(x, y)
    self.set_turtle_pos(x, y)
    
    self._add_state()
    self._add_action(ActionType.LINE_ABSOLUTE if self.pen else ActionType.MOVE_ABSOLUTE)
  
  def teleport(self, x, y):
    self.distance = 0
    self.set_turtle_pos(x, y)
    
    self._add_state()
    self._add_action(ActionType.MOVE_ABSOLUTE)
    
  def right(self, alpha):
    self.bearing = self.bearing - alpha
    
  def rt(self, alpha):
    self.right(alpha)
    
  def left(self, alpha):
    self.bearing = self.bearing + alpha
    
  def lt(self, alpha):
    self.left(alpha)
    
  def dot(self, size, *color):
    tmp_color = self.pencolor
    
    self.distance = 0
    self.radius = (size / 2) if size else max((self.pensize + 4) / 2, self.pensize)
    
    if len(color) == 3:
      r = self._clamp(color[0], 0, 255)
      g = self._clamp(color[1], 0, 255)
      b = self._clamp(color[2], 0, 255)
      
      self.pencolor = '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)
    else:
      if type(color[0]) is str:
        self.pencolor = color[0]
      else:
        self.pencolor = '#{0:02x}{1:02x}{2:02x}'.format(*color[0])
        
    self._add_action(self, ActionType.DRAW_DOT)
    self.pencolor = tmp_color
        
  def heading(self) -> float:
    self.bearing = (self.bearing % 360 + 360) % 360
    
    if Turtle.MODE == Mode.LOGO:
      return ((90 - self.bearing) % 360 + 360) % 360
    else:
      return self.bearing
    
  def setheading(self, bearing: float):
    if Turtle.MODE == Mode.LOGO:
      self.bearing = ((90 - bearing) % 360 + 360) % 360
    else:
      self.bearing = (bearing % 360 + 360) % 360
    
    self._add_state()
    
  def circle(self, radius: float, extent=None):
    if extent is None:
      extent = 360
    while extent >= 180:
      self.__circle(radius, 180)
      extent -= 180
    if extent > 0:
      self.__circle(radius, extent)
      
  def towards(self, *coordinates) -> None:
      if len(coordinates) == 1:
          x, y = coordinates[0]
      else:
          x, y = coordinates

      _x, _y = self.pos()
      dx = x - _x
      dy = y - _y
      return degrees(atan2(dy, dx))
    
  def hideturtle(self):
    self.show = False
      
    self._add_state()
      
  def ht(self):
    self.hideturtle()
    
  def showturtle(self):
    self.show = True
      
    self._add_state()
      
  def st(self):
    self.showturtle()
    
  def bgcolor(self, *args):
    if len(args) == 3:
      r = self._clamp(args[0], 0, 255)
      g = self._clamp(args[1], 0, 255)
      b = self._clamp(args[2], 0, 255)

      self.screen.background = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
    elif len(args) == 1:
      self.screen.background = args[0]
      
  def write(self, arg, align='left', font=("Arial", 8, "normal")):
    self.text = str(arg)
    self.align = align.lower()
    self.font = font
    self.distance = 0
    self._add_action(ActionType.WRITE_TEXT)
    self.text = None
    
  def play(self, sound):
    self.media = sound
    self.distance = 0
    self._add_action( ActionType.SOUND)
    self.media = None
    
  def save(self):
    self.screen.save()
    
  def _circle(self, radius, extent):
    _x, _y = self.pos()
    
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
    _x, _y = _x + self.radius * cos(alpha), _y - self.radius * sin(alpha)
    alpha = alpha - radians(180) + radians(extent)
    self.x, self.y = _x + self.radius * cos(alpha), _y - self.radius * sin(alpha)
    self.distance = self.radius * radians(abs(extent))
    
    self._add_state()
    self._add_action(ActionType.CIRCLE)
    
  def _distance(self, x, y):
    _x, _y = self.pos()
    
    return sqrt((_x - x) ** 2 + (_y - y) ** 2)
  
  def _clamp(self, num: int, low: int, high: int) -> int:
    return max(low, min(num, high))
