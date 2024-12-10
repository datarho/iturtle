import threading
import time
import uuid

from .frontend import MODULE_NAME, MODULE_VERSION
from IPython.display import clear_output, display
from enum import Enum
from ipywidgets import DOMWidget
from traitlets import Bool, Dict, Float, Int, List, Unicode

class ActionType(str, Enum):
  MOVE_ABSOLUTE = 'M'
  MOVE_RELATIVE = 'm'
  LINE_ABSOLUTE = 'L'
  DRAW_DOT = 'D'
  WRITE_TEXT = 'W'
  CIRCLE = 'C'
  SOUND = 'S'
  CLEAR = 'CLR'
  UPDATE_STATE= 'UPDATE_STATE'

SCREEN_FRAMERATE = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

class Screen(DOMWidget):
  _model_name = Unicode('TurtleModel').tag(sync=True)
  _model_module = Unicode(MODULE_NAME).tag(sync=True)
  _model_module_version = Unicode(MODULE_VERSION).tag(sync=True)
  _view_name = Unicode('TurtleView').tag(sync=True)
  _view_module = Unicode(MODULE_NAME).tag(sync=True)
  _view_module_version = Unicode(MODULE_VERSION).tag(sync=True)
  
  id = Unicode('').tag(sync=True)
  width = Int(SCREEN_WIDTH).tag(sync=True)
  height = Int(SCREEN_HEIGHT).tag(sync=True)
  bgUrl = Unicode("").tag(sync=True)
  background = Unicode("white").tag(sync=True)
  
  actions = List([]).tag(sync=True)
  
  def __init__(self, framerate=SCREEN_FRAMERATE):
    super(Screen, self).__init__()
    
    display(self)
    
    time.sleep(0.1)
    self.id = str(uuid.uuid4())
    
    self.todo_actions = []
    
    self.interval = 1000 / framerate
    self.stop_event = threading.Event()
    self.lock = threading.Lock()
    self.thread = None
    
    self.start()
    
  def start(self):
    if (not self.thread) or (not self.thread.is_alive()):
      self.stop_event.clear()
      self.thread = threading.Thread(target=self._run)
      self.thread.start()

  def stop(self):
    if self.thread:
      self.stop_event.set()
      self.thread.join()
      self.lock.release()
      
  def bgpic(self, src):
    self.bgUrl = src
      
  def save(self):
    clear_output()
    display(self)
      
  def add_action(self, action):
    try:
      self.lock.acquire()
      self.todo_actions.append(action)
    finally:
      self.lock.release()
      
  def _run(self):
    while not self.stop_event.is_set():
      next_timestamp = time.monotonic() + self.interval
      
      self.actions = self._build_actions()
      
      sleep_time = next_timestamp - time.monotonic()
      if sleep_time > 0:
        self.stop_event.wait(sleep_time / 1000)
  
  def _build_actions(self):
    _actions = []
    
    try:
      self.lock.acquire()
      
      for i in range(len(self.todo_actions)):
        _actions.append(self.todo_actions.pop(0))
        # 简化forward的处理，先瞬移再说
    finally:
      self.lock.release()

    return _actions
