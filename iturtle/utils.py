def build_color(mode, *_color):
  if (len(_color) == 1):
    if type(_color[0]) in [list, tuple]:
      _color = _color[0]
    elif type(_color[0]) is str:
      return _color[0]
  if len(_color) == 3:
    # in case not in int format
    _r, _g, _b = _color[0], _color[1], _color[2]
    if (_r <= 1) and (_g <= 1) and (_b <= 1):
      if mode == 1.0:
        _r = int(_r * 255)
        _g = int(_g * 255)
        _b = int(_b * 255)

    r = clamp(int(_r), 0, 255)
    g = clamp(int(_g), 0, 255)
    b = clamp(int(_b), 0, 255)
  
    return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)
  
def decode_color(mode, color):
  if color.startswith('#'):
    r = int('0x' + color[1:3], 16)
    g = int('0x' + color[3:5], 16)
    b = int('0x' + color[5:7], 16)
    
    return (r / 255, g / 255, b / 255) if (mode == 1.0) else (r, g, b)
  else:
    return color

def clamp(num: int, low: int, high: int) -> int:
  return max(low, min(num, high))