from typing import List
from controller.controller_inputs import ControllerInput
from display.display import Display
from display.font_purpose import FontPurpose
import sdl2
from devices.device import Device
from controller.controller import Controller
from themes.theme import Theme
from views.image_text_pair import ImageTextPair

class ImageListView:

    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, top_bar_text,
                 options: List[ImageTextPair], img_offset_x : int, img_offset_y : int):
        self.display = display
        self.controller = controller
        self.device = device
        self.theme = theme
        self.top_bar_text = top_bar_text
        self.options = options

        self.selected = 0
        self.toggles = [False] * len(options)
        self.line_height = display.get_line_height(FontPurpose.LIST) + 10  # add 10px padding between lines
        self.current_top = 0
        self.current_bottom = min(device.max_rows_for_list,len(options))
        self.img_offset_x = img_offset_x
        self.img_offset_y = img_offset_y
     

    def _render_text(self, visible_options):
        for visible_index, (imageTextPair) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
            color = self.theme.text_color_selected(FontPurpose.LIST) if actual_index == self.selected else self.theme.text_color(FontPurpose.LIST)
            self.display.render_text(imageTextPair.get_text(), 50, self.display.get_top_bar_height() + 5 + visible_index * self.line_height, color, FontPurpose.LIST)

    def _render_image(self, visible_options):
        for visible_index, (imageTextPair) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
            imagePath = imageTextPair.get_image_path_selected() if actual_index == self.selected else imageTextPair.get_image_path()
            if(actual_index == self.selected and imagePath is not None):
                self.display.render_image_centered(imagePath, 
                                     self.img_offset_x, 
                                     self.img_offset_y)

    def _render(self):
        self.display.clear(self.top_bar_text)
        self.selected = max(0, self.selected)
        self.selected = min(len(self.options)-1, self.selected)
        
        while(self.selected < self.current_top):
            self.current_top -= 1
            self.current_bottom -=1

        while(self.selected >= self.current_bottom):
            self.current_top += 1
            self.current_bottom +=1

        visible_options = self.options[self.current_top:self.current_bottom]

        #ensure image is rendered last so it is on top of the text
        self._render_text(visible_options)
        self._render_image(visible_options)

        self.display.present()

    def adjust_selected(self, amount):
        if(amount < 0):
            if(self.current_top + amount < 0):
                amount = -1 * self.selected
        elif(self.current_bottom - amount > len(self.options)):
                amount = self.current_bottom - self.selected

        self.selected += amount
        self.current_top += amount
        self.current_bottom += amount

    def get_selection(self):
        self._render()
        running = True
        
        while running:
            if(self.controller.get_input()):
                if self.controller.last_input() == ControllerInput.DPAD_UP:
                    self.selected-=1
                elif self.controller.last_input() == ControllerInput.DPAD_DOWN:
                    self.selected+=1
                elif self.controller.last_input() == ControllerInput.L1:
                    self.adjust_selected(-1*self.device.max_rows_for_list)
                elif self.controller.last_input() == ControllerInput.R1:
                    self.adjust_selected(self.device.max_rows_for_list)
                elif self.controller.last_input() == ControllerInput.A:
                    return self.options[self.selected]
                elif self.controller.last_input() == ControllerInput.B:
                    return None

                self._render()
