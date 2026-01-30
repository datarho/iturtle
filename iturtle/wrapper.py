from functools import wraps

from .turtle import Screen, Turtle, done


default_screen = None
default_turtle = None

# Screen wrappers
def check_default_screen():
  global default_screen
  
  if default_screen is None:
    default_screen = Screen()
    
  return default_screen

def screensize(width, height, *_color):
  screen = check_default_screen()
  
  if screen:
    screen.setup(width, height)
    screen.bgcolor(*_color)
    
def tracer(n):
  screen = check_default_screen()
  
  if screen:
    screen.tracer(n)

# Turtle wrappers
def check_default_turtle():
  global default_turtle
  
  screen = check_default_screen()

  if not default_turtle:
    default_turtle = Turtle(screen)
    
  return default_turtle

def turtle_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = check_default_turtle()
        if t:
            method = getattr(t, func.__name__, None)
            if method:
                return method(*args, **kwargs)
        return None
    return wrapper

@turtle_method
def showturtle():
  pass

@turtle_method
def hideturtle():
  pass

@turtle_method
def isvisible():
  pass

@turtle_method
def reset():
  pass

@turtle_method
def xcor():
  pass

@turtle_method
def ycor():
  pass

@turtle_method
def pos():
  pass

@turtle_method
def position():
  pass

@turtle_method
def setx(x):
  pass

@turtle_method
def sety(y):
  pass

@turtle_method
def speed(_speed=None):
  pass

@turtle_method
def colormode(mode=None):
  pass

@turtle_method
def color(*_color):
  pass

@turtle_method
def fillcolor(*_color):
  pass

@turtle_method
def heading():
  pass

@turtle_method
def setheading(angle):
  pass

@turtle_method
def towards(x, y=None):
  pass

@turtle_method
def bgcolor(*_color):
  pass

@turtle_method
def shape(_shape=None, reload=False):
  pass

@turtle_method
def shapesize(stretch_wid=None, stretch_len=None, outline=None):
  pass

@turtle_method
def penup():
  pass

@turtle_method
def pendown():
  pass

@turtle_method
def isdown():
  pass

@turtle_method
def pencolor(*color):
  pass

@turtle_method
def pensize(size):
  pass

@turtle_method
def distance(x, y=None):
  pass

@turtle_method
def backward(distance):
  pass

@turtle_method
def forward(distance):
  pass

@turtle_method
def goto(x, y=None, *, need_delay=True):
  pass

@turtle_method
def teleport(x, y=None):
  pass

@turtle_method
def stamp():
  pass

@turtle_method
def home():
  pass

@turtle_method
def left(angle):
  pass

@turtle_method
def right(angle):
  pass

@turtle_method
def clear():
  pass

@turtle_method
def play(sound, reload=False):
  pass

@turtle_method
def write(arg, move=False, align='left', font=("Arial", 8, "normal")):
  pass

@turtle_method
def dot(size=1, color=None):
  pass

@turtle_method
def circle(radius, extent=360):
  pass

@turtle_method
def begin_fill():
  pass

@turtle_method
def end_fill():
  pass

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

mainloop = done