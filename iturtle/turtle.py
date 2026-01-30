import queue
import threading
import sys
import time
import uuid

from .screen import Screen
from .utils import build_color, decode_color
from math import atan2, cos, degrees, radians, sin, sqrt
from traitlets import Enum

ACTIVE_TURTLES = set()
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
  BEGIN_FILL = 'BEGIN_FILL'
  END_FILL = 'END_FILL'
  DONE = 'DONE'

def turtle_worker(*args):
  screen = args[0]
  queue = args[1]
  stop_event = args[2]
  
  while not stop_event.is_set():
    try:
      action = queue.get(block=True, timeout=3)
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
    except Exception:
      pass

def set_active(func):
  def wrapper(*args, **kwargs):
    ACTIVE_TURTLES.add(args[0])
        
    return func(*args, **kwargs)
  return wrapper
  
class Turtle:
  @staticmethod
  def input(prompt=''):
    kernel = get_ipython().kernel
    msg_header = {
      'msg_id': kernel.session.msg_id,   # 生成唯一的消息 ID
      'msg_type': 'input_request',       # 消息类型
      'username': 'kernel',              # 用户名
      'session': kernel.session.session, # 会话 ID
      'version': '5.0'                   # 协议版本
    }
    kernel.session.send(
      stream=kernel.stdin_socket,
      msg_or_type='input_request',
      content={'prompt':  prompt, "password": False },
      parent=kernel.get_parent("shell"),
      ident=kernel._parent_ident["shell"],
      header=msg_header,
      metadata= { 'type': 'iturtle' }
    )
    
    while True:
      msg = kernel.session.recv(kernel.stdin_socket)
      if msg and msg[1]:
        _msg = msg[1]
        if _msg['msg_type'] == 'input_reply':
          return _msg['content']['value']
      time.sleep(2)
  
  def __init__(self, screen=None):
    if screen is None:
      self.screen = Screen()
    else:
      self.screen = screen
    
    self.stop_event = threading.Event()
    self._queue = queue.Queue()
    
    self._thread = threading.Thread(target=turtle_worker, args=(self.screen, self._queue, self.stop_event))
    self._thread.start()
    
    self.id = str(uuid.uuid4())
    
    self._init()
    
    self.penup()
    self.home()
    self.pendown()
    
    ACTIVE_TURTLES.add(self)
    
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
    self._clockwise = 1
    self._large_arc = 0
    self._media = None
    self._shape = ''
    self._text = ''
    self._align = 'left'
    self._font = ('Arial', 8, 'normal')
    self._fill_mode = False # Default not in fill node
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def __del__(self):
    self.stop_event.set()
    self._thread.join()
    
  def done(self):
    self._add_action(ActionType.DONE, False)
    
  def _add_action(self, action_type, need_delay=True):
    if not self.stop_event.is_set():
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
        'large_arc': self._large_arc,
        'media': self._media,
        'shape': self._shape,
        'need_delay': need_delay,
        'fill_mode': self._fill_mode,
      }
      
      if (action_type == ActionType.WRITE_TEXT) and self._text:
        action['text'] = self._text
        action["font"] = self._font
        action["align"] = self._align    
        
      # self.screen.add_action(action)
      self._queue.put(action)
    
  @set_active
  def showturtle(self):
    self._show = True
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  @set_active
  def hideturtle(self):
    self._show = False
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  def isvisible(self):
    return self._show
  
  @set_active
  def reset(self):
    self.clear()
    self._init()
  
  def xcor(self):
    return self._x
  
  def ycor(self):
    return self._y
  
  def position(self):
    return (self._x, self._y)

  @set_active
  def setx(self, x):
    self._x = x
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    
    self._add_action(ActionType.UPDATE_STATE, False)

  @set_active
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

  def colormode(self, mode=None):
    if mode is None:
      return self.screen.colormode()
    else:
      self.screen.colormode(mode)

  def color(self, *_color):
      if not _color:
        return decode_color(self.screen.colormode(), self._color)
      else:
        if len(_color) == 1:
          self._color = build_color(self.screen.colormode(), *_color)
          self._pencolor = self._color
        elif len(_color) == 2:
          self._pencolor = build_color(self.screen.colormode(), _color[0])
          self._color = build_color(self.screen.colormode(), _color[1])
        else:
          self._color = build_color(self.screen.colormode(), *_color)
          self._pencolor = self._color
        
        self._add_action(ActionType.UPDATE_STATE, False)

  def fillcolor(self, *_color):
    if not _color:
      return decode_color(self.screen.colormode(), self._color)
    else:
      self._color = build_color(self.screen.colormode(), *_color)
      
      self._add_action(ActionType.UPDATE_STATE, False)

  def heading(self):
    return self._heading

  @set_active
  def setheading(self, angle):
    self._heading = (angle + 360) % 360
    
    self._add_action(ActionType.UPDATE_STATE, False)

  @set_active
  def towards(self, x, y=None):
    _x, _y = 0, 0
    if y is None:
      if type(x) in [list, tuple]:
        _x, _y = x[0], x[1]
      else:
        _x, _y = x, self._y
    else:
      _x, _y = x, y
      
    return degrees(atan2(_y - self._y, _x - self._x))

  @set_active
  def bgcolor(self, *_color): # Same as for screen
    if not _color:
      return self.screen.bgcolor()
    else:
      self.screen.bgcolor(*_color)

  @set_active
  def shape(self, _shape=None, reload=False):
    if _shape not in ['circle', 'default', 'square', 'triangle', 'turtle']:
      self.screen.load(_shape, reload)
        
    if _shape is None:
      return self._shape
    else:
      self._shape = _shape
      
    self._add_action(ActionType.UPDATE_STATE, False)

  @set_active
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
      return decode_color(self.screen.colormode(), self._pencolor)
    else:
      self._pencolor = build_color(self.screen.colormode(), *color)
      
    self._add_action(ActionType.UPDATE_STATE, False)

  def pensize(self, size):
    self._pensize = size
    
    self._add_action(ActionType.UPDATE_STATE, False)

  def distance(self, x, y=None):
    _x, _y = 0, 0
    
    if y is None:
      if (type(x) is list) or (type(x) is tuple):
        _x, _y = x._x, x._y
      elif (type(x) is list) or (type(x) is tuple):
        _x, _y = x[0], x[1]
      else:
        _x, _y = x, self._y
    else:
      _x, _y = x, y
      
    return sqrt((self._x - _x) ** 2 + (self._y - _y) ** 2)

  @set_active
  def backward(self, distance):
    self.forward(-distance)
    
  @set_active
  def forward(self, distance):
    angle = radians(self._heading)
    
    self._x += distance * cos(angle)
    self._y += distance * sin(angle)
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    self._distance = distance
    
    self._add_action(ActionType.LINE_ABSOLUTE if self._pen else ActionType.MOVE_ABSOLUTE)

  @set_active
  def goto(self, x, y=None, *, need_delay=True):
    if (y == None) and (type(x) in [list, tuple]):
      x, y = x[0], x[1]

    self._distance = self.distance(x, y)
    self._x = x
    self._y = y
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    
    self._add_action(ActionType.LINE_ABSOLUTE if self._pen else ActionType.MOVE_ABSOLUTE, need_delay)

  @set_active
  def teleport(self, x, y=None):
    if (y == None) and (type(x) in [list, tuple]):
      x, y = x[0], x[1]
      
    self._distance = 0
    self._x = x
    self._y = y
    self._canvas_position = self._to_canvas_pos(self._x, self._y)
    
    self._add_action(ActionType.MOVE_ABSOLUTE)

  @set_active
  def stamp(self):
    self._stampid = str(uuid.uuid4())
    self._add_action(ActionType.STAMP, False)
    
    self._stampid = ''

  @set_active
  def home(self):
    self._heading = DEFAULT_HEADING
    self.goto(0, 0)

  @set_active
  def left(self, angle):
    self._heading += angle
    
    self._add_action(ActionType.UPDATE_STATE, False)

  @set_active
  def right(self, angle):
    self._heading -= angle
    
    self._add_action(ActionType.UPDATE_STATE, False)
    
  @set_active
  def clear(self):
    self._add_action(ActionType.CLEAR, False)

  @set_active
  def play(self, sound, reload=False): # iturtle specific
    self.screen.load(sound, reload)
    
    self._media = sound
    self._distance = 0
    self._add_action( ActionType.SOUND, False)
    self._media = None

  @set_active
  def write(self, arg, move=False, align='left', font=("Arial", 8, "normal")):
    self._text = str(arg)
    self._align = align.lower()
    self._font = font
    self._distance = 0
    self._add_action(ActionType.WRITE_TEXT, False)
    self.text = None

  @set_active
  def dot(self, size=1, color=None):
    tmp_color = self._pencolor
    
    self._distance = 0
    # self._radius = (size / 2) if size else 0.5
    if size is None:
      self.radius = max((self._pensize + 4) / 2, self._pensize)
    else:
      self._radius = (size / 2)
    
    if color is not None:
      self._pencolor = build_color(self.screen.colormode(), color)
        
    self._add_action(ActionType.DRAW_DOT)
    self._pencolor = tmp_color
  
  '''
  Guidelines for Drawing Circles
  1. SVG Constraint: Due to limitations in SVG, a full circle must be rendered as two semicircular arcs.
  2. _circle Function Behavior:
    - The _circle function handles the rendering of individual circular arcs. Its behavior depends on the sign of the radius:
      - Positive Radius:
        - Arcs are drawn counterclockwise.
        - The center is positioned 90° to the left of the current heading.
        - The arc angle (in radians) remains positive.
      - Negative Radius:
        - Arcs are drawn clockwise.
        - The center is positioned 90° to the right of the current heading.
        - The arc angle is negated (i.e., treated as a negative value).
    - Additional Steps:
      - Compute the center coordinates based on the current position and heading.
      - Determine the endpoint of the arc using the center and the specified angle.
      - Update the current heading to reflect the new orientation after drawing the arc.
      - If the input angle (in degrees) is greater than 180°, set the large_arc flag to 1.
  '''
  @set_active
  def circle(self, radius, extent=360):
    while extent >= 360:
      self._circle(radius, 180)
      extent -= 180

    if extent > 0:
      self._circle(radius, extent)
    
  def _circle(self, radius, extent):   
    self._clockwise = 0 if radius > 0 else 1
    _dir = -90 if self._clockwise else 90
    _extent = -extent if self._clockwise else extent
    
    if radius != 0:
      radius = abs(radius)
      angle_to_center  = radians(self._heading + _dir)
      extent_rad  = radians(_extent)
      
      delta_x = radius * cos(angle_to_center)
      delta_y = radius * sin(angle_to_center)
      x0 = self._x + delta_x
      y0 = self._y + delta_y
      
      self._radius = abs(radius)
      self._x = x0 + (-delta_x) * cos(extent_rad) - (-delta_y) * sin(extent_rad)
      self._y = y0 + (-delta_x) * sin(extent_rad) + (-delta_y) * cos(extent_rad)
      
      self._heading += _extent
      self._large_arc = 1 if extent > 180 else 0
      self._distance = self._radius * radians(abs(extent))
      self._canvas_position = self._to_canvas_pos(self._x, self._y)
      
      self._add_action(ActionType.CIRCLE)

  @set_active
  def begin_fill(self):
    self._fill_mode = True
    
    self._add_action(ActionType.BEGIN_FILL)

  @set_active
  def end_fill(self):
    self._fill_mode = False
    
    self._add_action(ActionType.END_FILL)

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
  pos = position

  bk = backward
  back = backward
  fd = forward
  setpos = goto
  setposition = goto

def done():
  screens = set()
  for t in ACTIVE_TURTLES:
    if t.screen not in screens:
      t.done()
      screens.add(t.screen)

  ACTIVE_TURTLES.clear()