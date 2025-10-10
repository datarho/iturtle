import base64
import threading
import time
import uuid

from .frontend import MODULE_NAME, MODULE_VERSION
from .utils import build_color, decode_color
from IPython.display import clear_output, display
from ipywidgets import DOMWidget
from traitlets import Dict, HasTraits, Int, List, Unicode, observe

SCREEN_FRAMERATE = 15
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
DELAY = 2
# SCREEN_WIDTH = 500
# SCREEN_HEIGHT = 800

IMAGE_EXTS = ['bmp', 'gif', 'ico‌', 'jpg', 'png', 'svg']
VIDEO_EXTS = ['mp4', 'webm']
AUDIO_EXTS = ['aac', 'm4a', 'mp3', 'wav']

class Screen(DOMWidget, HasTraits):
  _model_name = Unicode('TurtleModel').tag(sync=True)
  _model_module = Unicode(MODULE_NAME).tag(sync=True)
  _model_module_version = Unicode(MODULE_VERSION).tag(sync=True)
  _view_name = Unicode('TurtleView').tag(sync=True)
  _view_module = Unicode(MODULE_NAME).tag(sync=True)
  _view_module_version = Unicode(MODULE_VERSION).tag(sync=True)
  
  id = Unicode('').tag(sync=True)
  width = Int(SCREEN_WIDTH).tag(sync=True)
  height = Int(SCREEN_HEIGHT).tag(sync=True)
  delay = Int(DELAY).tag(sync=True)
  bgUrl = Unicode('').tag(sync=True)
  background = Unicode("white").tag(sync=True)
  resource = Dict().tag(sync=True)
  
  key = Unicode('').tag(sync=True)
  actions = List([]).tag(sync=True)
  
  def __init__(self, framerate=SCREEN_FRAMERATE):
    super(Screen, self).__init__()
    
    self._tracer = 1 # 0 means manual mode, others as auto mode
    self._colormode = 1.0 # or 255
    self.curr_key = None
    self._on_keys = {}
    self._framerate = SCREEN_FRAMERATE
    
    self.loaded = set()
    
    display(self)
    
    time.sleep(0.1)
    self.id = str(uuid.uuid4())
    
    self.todo_actions = {}
    
    self._main_loop = None
    
    
    self.interval = 1000 / framerate
    self.stop_event = threading.Event()
    self.lock = threading.Lock()
    self.thread = None
    
    if self._tracer > 0:
      self.start()

  def setup(self, width, height):
      self.width = width
      self.height = height
    
  def start(self, main_loop=None):
    if (not self.thread) or (not self.thread.is_alive()):
      self.stop_event.clear()
      self.thread = threading.Thread(target=main_loop if main_loop else self._run)
      self.thread.start()

  def stop(self):
    if self.thread:
      self.stop_event.set()
      self.thread.join()
      if self.lock.locked():
        self.lock.release()
      
  def tracer(self, n):
    self._tracer = n
    
    if self._tracer > 0:
      self.start()
    else:
      self.stop()
      
  def colormode(self, mode=None):
    if mode is None:
      return self._colormode
    else:
      if (mode == 1.0) or (mode == 255):
        self._colormode = mode
      
  def update(self):
    if self._tracer == 0:
      _actions = self._build_actions()
      if len(_actions) > 0:
        self.actions = _actions
      
  def bgcolor(self, *_color):
    if not _color:
      return decode_color(self._colormode, self.background)
    else:
      self.background = build_color(self._colormode, *_color)
      
  def bgpic(self, src, reload=False):
    self.load(src, reload)
    
    self.bgUrl = src
      
  def save(self):
    clear_output()
    display(self)
    
  def onkeypress(self, fn, key):
    self._on_keys[key] = fn
      
  def add_action(self, action):
    try:
      self.lock.acquire()

      _id = action['id']
      if _id not in self.todo_actions:
        self.todo_actions[_id] = []
      self.todo_actions[_id].append(action)
    finally:
      self.lock.release()
      
  def load(self, file_path, reload=False):
    if (file_path not in self.loaded) or reload:
      if not ((file_path.startswith('http://')) or (file_path.startswith('https://'))):
        ext = file_path.split('.')[-1].lower()
        _type = None
        
        if ext in IMAGE_EXTS:
          _type = 'image'
        elif ext in VIDEO_EXTS:
          _type = 'video'
        elif ext in AUDIO_EXTS:
          _type = 'audio'
        else:
          raise Exception(f'Unknown resource type for {file_path}')

        if ext == 'svg':
          buffer = read_file(file_path).decode('ascii')
        else:
          buffer = file_to_base64(file_path)

        self.resource = {
          'name': file_path,
          'type': _type,
          'ext': ext,
          'buffer': buffer
        }
    
        self.loaded.add(file_path)
      
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
      
      # 简化处理，先瞬移再说  
      for v in self.todo_actions.values():
        for _ in range(len(v)):
          _actions.append(v.pop(0))
    finally:
      self.lock.release()

    return _actions
  
  @observe('key')
  def on_key_change(self, _):
    self.curr_key = self.key
    
    if self.curr_key in self._on_keys:
      (self._on_keys[self.curr_key])()
    
    self.curr_key = None

def read_file(file_path):
  with open(file_path, 'rb') as f:
    return f.read()
  
def file_to_base64(file_path):
  fc = read_file(file_path)
  buffer = base64.b64encode(fc)
  
  return buffer.decode('utf-8')