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
    def font_size_small(self):
        return 12
    
    @property
    def font_size_medium(self):
        return 18
    
    @property
    def font_size_large(self):
        return 26

    @property
    def max_rows_for_list(self):
        return 12
    
    #Can we dynamically calculate these?
    @property
    def max_icons_for_large_grid_view(self):
        return 4
    
    @property
    def large_grid_x_offset(self):
        return 34

    @property
    def large_grid_y_offset(self):
        return 160
    
    @property
    def large_grid_spacing_multiplier(self):
        icon_size = 140
        return icon_size+int(self.large_grid_x_offset/2)
