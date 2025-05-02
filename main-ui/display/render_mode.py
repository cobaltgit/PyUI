from enum import Enum, auto

class RenderMode(Enum):
    ABSOLUTE = auto()
    X_CENTERED = auto()
    XY_CENTERED = auto()
    TOP_RIGHT_ADJUST = auto() # Top Right Pixel will be at passed in (x,y)