import queue
import threading
import time
import uuid

from .screen import Screen
from math import atan2, cos, degrees, radians, sin, sqrt
from traitlets import Enum

DEFAULT_HEADING = 0

class ActionType(str, Enum):
  MOVE_ABSOLUTE = 'M'
  MOVE_RELATIVE = 'm'
  LINE_ABSOLUTE = 'L'
  DRAW_DOT = 'D'
  WRITE_TEXT = 'W'
  CIRCLE = 'C'
  SOUND = 'S'
  CLEAR = 'CLR'
  UPDATE_STATE = 'UPDATE_STATE'
  STAMP = 'STAMP'

def turtle_worker(*args):
  screen = args[0]
  action_queue = args[1]
  
  while True:
    action = action_queue.get()
    if action:
      delay = 0.02
      if action['need_delay']:
        distance = action['distance']
        speed = action['speed']
        
        if speed < 10:
          delay = max(
            abs(distance) * screen.delay / (3 * 1.1 ** speed * speed),
            1
          ) * 0.05
          
        time.sleep(delay)
        
      screen.add_action(action)

class Turtle:
  def __init__(self, screen=None):
    if screen is None:
      self.screen = Screen()
    else:
      self.screen = screen
    
    self._queue = queue.Queue()
    
    self._thread = threading.Thread(target=turtle_worker, args=(self.screen, self._queue))
    self._thread.start()
    
    self.id = str(uuid.uuid4())
    
    self._init()
    
    self.penup()
    self.home()
    self.pendown()
    
  def _init(self):
    self._stretchfactor = (1, 1)
    self._outlinewidth = 1
    
    self._x = 0
    self._y = 0
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    self._speed = 10
    self._color = 'black'
    self._heading = DEFAULT_HEADING
    self._show = True
    self._stampid = ''
    self._pen = True
    self._pencolor = 'black'
    self._pensize = 1
    self._penstretchfactor = self._stretchfactor
    self._penoutlinewidth = self._outlinewidth
    self._distance = 0
    self._radius = 0
    self._clockwise = 1 # TODO to bool
    self._media = None
    self._shape = ''
    self._text = ''
    self._align = 'left'
    self._font = ('Arial', 8, 'normal')
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def _add_action(self, action_type, need_delay=True):
    action = {
      'id': self.id,
      'type': action_type,
      'position': self._canvas_position,
      'speed': self._speed,
      'color': self._color,
      'heading': self._heading,
      "show": self._show,
      'stampid': self._stampid,
      'pen': self._pen,
      'pencolor': self._pencolor,
      'pensize': self._pensize,
      'penstretchfactor': self._penstretchfactor,
      'penoutlinewidth': self._penoutlinewidth,
      'distance': abs(self._distance),
      'radius': self._radius,
      'clockwise': self._clockwise,
      'media': self._media,
      'shape': self._shape,
      'need_delay': need_delay
    }
    
    if (action_type == ActionType.WRITE_TEXT) and self._text:
      action['text'] = self._text
      action["font"] = self._font
      action["align"] = self._align    
      
    # self.screen.add_action(action)
    self._queue.put(action)
    
  # State
  def showturtle(self):
    self._show = True
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def hideturtle(self):
    self._show = False
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def isvisible(self):
    return self._show
  
  def reset(self):
    self.clear()
    self._init()
  
  def xcor(self):
    return self._x
  
  def ycor(self):
    return self._y
  
  def pos(self):
    return self.position()
  
  def position(self):
    return (self._x, self._y)
  
  def setx(self, x):
    self._x = x
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def sety(self, y):
    self._y = y
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    
    self._add_action(ActionType.UPDATE_STATE, False)

  def speed(self, _speed=None):
    if _speed is None:
      return self._speed
    else:
      self._speed = 10
      
      if type(_speed) is str:
        if _speed == 'fastest':
          self._speed = 10
        elif _speed == 'fast':
          self._speed = 10
        elif _speed == 'normal':
          self._speed = 6
        elif _speed == 'slow':
          self._speed = 3
        elif _speed == 'slowest':
          self._speed = 1
      else:
        if 0.5 < _speed < 10.5:
          self._speed = int(round(_speed))
          
  def color(self, *_color):
      if not _color:
        return self._color
      else:
        self._color = build_color(*_color)
        self._pencolor = self._color
        
        self._add_action(ActionType.UPDATE_STATE, False)

  def heading(self):
    return self._heading
    
  def setheading(self, angle):
    self._heading = (angle + 360) % 360
    
    self._add_action(ActionType.UPDATE_STATE, False)

  def towards(self, x, y=None):
    _x, _y = 0, 0
    if y is None:
      if (type(x) is list) or (type(x) is tuple):
        _x, _y = x[0], x[1]
      else:
        _x, _y = x, self._y
    else:
      _x, _y = x, y
      
    return degrees(atan2(_y - self._y, _x - self._x))
  
  def bgcolor(self, *args): # Same as for screen
    if len(args) == 3:
      r = clamp(args[0], 0, 255)
      g = clamp(args[1], 0, 255)
      b = clamp(args[2], 0, 255)

      self.screen.background = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
    elif len(args) == 1:
      self.screen.background = args[0]
      
  def shape(self, _shape=None, reload=False):
    if _shape not in ['circle', 'default', 'square', 'triangle', 'turtle']:
      self.screen.load(_shape, reload)
        
    if _shape is None:
      return self._shape
    else:
      self._shape = _shape
      
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):
    if stretch_wid is stretch_len is outline is None:
      stretch_wid, stretch_len = self._stretchfactor
      return self._stretchfactor[0], self._stretchfactor[1], self._outlinewidth
    
    if stretch_wid == 0 or stretch_len == 0:
      raise Exception('stretch_wid/stretch_len must not be zero')
    
    if stretch_wid is not None:
      if stretch_len is None:
        self._penstretchfactor = stretch_wid, stretch_wid
      else:
        self._penstretchfactor = stretch_wid, stretch_len
    elif stretch_len is not None:
      self._penstretchfactor = self._stretchfactor[0], stretch_len

    if outline is None:
      self._penoutlinewidth = self._outlinewidth
    else:
      self._penoutlinewidth = outline
      
  def penup(self):
    self._pen = False
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def pendown(self):
    self._pen = True
    
    self._add_action(ActionType.UPDATE_STATE, False)
  
  def isdown(self):
    return self._pen
  
  def pencolor(self, *color):
    if not color:
      return self._pencolor
    else:
      self._pencolor = build_color(*color)
      
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def pensize(self, size):
    self._pensize = size
    
    self._add_action(ActionType.UPDATE_STATE, False)
      
  # Move
  def distance(self, x, y=None):
    _x, _y = 0, 0
    
    if y is None:
      if type(x) is Turtle:
        _x, _y = x._x, x._y
      elif (type(x) is list) or (type(x) is tuple):
        _x, _y = x[0], x[1]
      else:
        _x, _y = x, self._y
    else:
      _x, _y = x, y
      
    return sqrt((self._x - _x) ** 2 + (self._y - _y) ** 2)
    
  def backward(self, distance):
    self.forward(-distance)
    
  def forward(self, distance):
    angle = radians(self._heading)
    
    self._x += distance * cos(angle)
    self._y += distance * sin(angle)
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    self._distance = distance
    
    self._add_action(ActionType.LINE_ABSOLUTE if self._pen else ActionType.MOVE_ABSOLUTE)
     
  def goto(self, x, y, need_delay=True):
    self._distance = self.distance(x, y)
    self._x = x
    self._y = y
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    
    self._add_action(ActionType.LINE_ABSOLUTE if self._pen else ActionType.MOVE_ABSOLUTE, need_delay)
    
  def teleport(self, x, y): # iturtle specific
    self._distance = 0
    self._x = x
    self._y = y
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    
    self._add_action(ActionType.MOVE_ABSOLUTE)
    
  def stamp(self):
    self._stampid = str(uuid.uuid4())
    self._add_action(ActionType.STAMP, False)
    
    self._stampid = ''
    
  def home(self):
    self._heading = DEFAULT_HEADING
    self.goto(0, 0)

  def left(self, angle):
    self._heading += angle

  def right(self, angle):
    self._heading -= angle
    
  # Draw
  def clear(self):
    self._add_action(ActionType.CLEAR, False)
    
  def play(self, sound, reload=False): # iturtle specific
    self.screen.load(sound, reload)
    
    self._media = sound
    self._distance = 0
    self._add_action( ActionType.SOUND, False)
    self._media = None
    
  def write(self, arg, move=False, align='left', font=("Arial", 8, "normal")):
    self._text = str(arg)
    self._align = align.lower()
    self._font = font
    self._distance = 0
    self._add_action(ActionType.WRITE_TEXT, False)
    self.text = None
    
  def dot(self, size=1, color=None):
    tmp_color = self._pencolor
    
    self._distance = 0
    self._radius = (size / 2) if size else 0.5
    
    if color is not None:
      self._pencolor = build_color(color)
        
    self._add_action(ActionType.DRAW_DOT)
    self._pencolor = tmp_color
    
  def circle(self, radius, extent=None):
    if extent is None:
      extent = 360
    while extent >= 360:
      self._circle(radius, 180)
      extent -= 180
    if extent > 0:
      self._circle(radius, extent)
      
  def _circle(self, radius, extent):
    if radius > 0:
      angle = radians(-self._heading - 90)
      extent = -abs(extent)
      self._clockwise = 0
    else:
      angle = radians(-self._heading + 90)
      extent = abs(extent)
      self.clockwise = 1
    self._heading -= extent
    
    self._radius = abs(radius)
    self._x += self._radius * cos(angle)
    self._y -= self._radius * sin(angle)
    angle -= (radians(180) + radians(extent))
    self._x += self._radius * cos(angle)
    self._y -= self._radius * sin(angle)
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    
    self._distance = self._radius * radians(abs(extent))
    
    self._add_action(ActionType.CIRCLE)

  def _to_canvas_pos(self, x, y):
    return x + self.screen.width / 2, self.screen.height / 2 - y
  
  st = showturtle
  ht = hideturtle
  seth = setheading
  turtlesize=shapesize
  lt = left
  rt = right
  pu = penup
  up = penup
  pd = pendown
  down = pendown
  width = pensize

  bk = backward
  back = backward
  fd = forward
  setpos = goto
  setposition = goto
  
def build_color(*_color):
  if (len(_color) == 1):
    if type(_color[0]) is str:
      return _color
    elif type(_color[0]) in [list, tuple]:
      _color = _color[0]
  if len(_color) == 3:
    # in case not in int format
    _r, _g, _b = _color[0], _color[1], _color[2]
    if (_r <= 1) and (_g <= 1) and (_b <= 1):
      _r = int(_r * 255)
      _g = int(_g * 255)
      _b = int(_b * 255)

    r = clamp(_r, 0, 255)
    g = clamp(_g, 0, 255)
    b = clamp(_b, 0, 255)
  
    return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)  

def clamp(num: int, low: int, high: int) -> int:
  return max(low, min(num, high))