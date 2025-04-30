from devices.device import Device
import os

os.environ["SDL_VIDEODRIVER"] = "KMSDRM"
os.environ["SDL_RENDER_DRIVER"] = "kmsdrm"

class MiyooFlip(Device):
    
    def __init__(self):
        self.path = self
    
    @property
    def screen_width(self):
        return 640

    @property
    def screen_height(self):
        return 480

    @property
    def font_size(self):
        return 28

    @property
    def max_rows_for_list(self):
        return 8