

from enum import Enum, auto


class ResizeType(Enum):
    FIT = auto(), #e.g. aspect ratio will remain identical
    ZOOM = auto(), #e.g.  The smaller dimension will be used as the base and the larger dimension cropped