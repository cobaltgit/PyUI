from typing import List
from controller.controller_inputs import ControllerInput
from display.font_purpose import FontPurpose
from display.font_size import FontSize
from display.display import Display
import sdl2
from devices.device import Device
from controller.controller import Controller
from themes.theme import Theme
from views.image_text_pair import ImageTextPair

class GridView:

    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, top_bar_text, options: List[ImageTextPair], cols : int, rows: int,):
        self.display : Display = display
        self.controller : Controller = controller
        self.device : Device = device
        self.theme : Theme = theme
        self.top_bar_text = top_bar_text
        self.options : List[ImageTextPair] = options 

        self.selected = 0
        self.toggles = [False] * len(options)

        self.current_left = 0
        self.current_right = min(rows * cols,len(options))

        self.rows = rows
        self.cols = cols
        if(rows > 1):
            self.font_purpose = FontPurpose.GRID_MULTI_ROW
            self.font_bg_pad = 12
            self.font_pad = 0
        else:
            self.font_purpose = FontPurpose.GRID_ONE_ROW
            self.font_bg_pad = 0
            self.font_pad = 15
     
    def _render(self):
        self.display.clear(self.top_bar_text)
        self.selected = max(0, self.selected)
        self.selected = min(len(self.options)-1, self.selected)
        
        while(self.selected < self.current_left):
            self.current_left -= (self.cols*2)
            self.current_right -= (self.cols*2)

        while(self.selected >= self.current_right):
            self.current_left += (self.cols*2)
            self.current_right += (self.cols*2)

        visible_options: List[ImageTextPair] = self.options[self.current_left:self.current_right]

        x_pad = 9 * self.cols
        usable_width = self.device.screen_width - (2 * x_pad)
        icon_width = usable_width / self.cols  # Initial icon width

        y_pad = self.display.get_top_bar_height() + 5
        usable_height = self.device.screen_height - (2 * y_pad)
        icon_height = usable_height / self.rows  # Initial icon width
        total_gap_height =  (self.rows - 1) * 10 if self.rows > 1 else 0
        y_gap = total_gap_height / (self.rows - 1)  if self.rows > 1 else 0

        text_pad = 20
        
        for visible_index, imageTextPair in enumerate(visible_options):

            actual_index = self.current_left + visible_index
            imagePath = imageTextPair.get_image_path_selected() if actual_index == self.selected else imageTextPair.get_image_path()
            
            x_index = visible_index % self.cols
            x_offset = int(x_pad + x_index * (icon_width)) + int(icon_width/2)

            if(self.rows == 1) : 
                y_offset = int(usable_height / 3) + y_pad
            else :
                y_index = int(visible_index / self.cols) 
                y_offset = int(y_pad + y_index * (icon_height + y_gap))

            font_bg_pad = 0
            if(imageTextPair.get_image_path_selected_bg() is not None):
                font_bg_pad = self.font_bg_pad
                if(actual_index == self.selected):
                    self.display.render_image_centered(imageTextPair.get_image_path_selected_bg(), 
                                            x_offset, 
                                            y_offset)

            actual_height, actual_width = self.display.render_image_centered(imagePath, 
                                     x_offset, 
                                     y_offset)
            color = self.theme.text_color_selected(self.font_purpose) if actual_index == self.selected else self.theme.text_color(self.font_purpose)
            self.display.render_text_centered(imageTextPair.get_text(), 
                                    x_offset,
                                    int(y_offset+actual_height - font_bg_pad + self.font_pad), color,
                                    self.font_purpose)
            
        self.display.present()

    def get_selection(self):
        self._render()
        running = True
        
        while running:
            if(self.controller.get_input()):
                if self.controller.last_input() == ControllerInput.DPAD_LEFT:
                    self.selected-=1
                elif self.controller.last_input() == ControllerInput.DPAD_RIGHT:
                    self.selected+=1
                elif self.controller.last_input() == ControllerInput.L1:
                    self.selected-=1
                elif self.controller.last_input() == ControllerInput.R1:
                    self.selected+=1
                if self.controller.last_input() == ControllerInput.DPAD_UP:
                    self.selected-=self.cols
                elif self.controller.last_input() == ControllerInput.DPAD_DOWN:
                    self.selected+=self.cols
                elif self.controller.last_input() == ControllerInput.A:
                    return self.options[self.selected]
                elif self.controller.last_input() == ControllerInput.B:
                    return None

                self._render()
