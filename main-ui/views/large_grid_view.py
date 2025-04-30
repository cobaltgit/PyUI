from typing import List
from screen.font_size import FontSize
from screen.screen import Screen
import sdl2
from devices.device import Device
from controller.controller import Controller
from themes.theme import Theme
from views.image_text_pair import ImageTextPair

class LargeGridView:

    def __init__(self, screen: Screen, controller: Controller, device: Device, theme: Theme, options: List[ImageTextPair]):
        self.screen : Screen = screen
        self.controller : Controller = controller
        self.device : Device = device
        self.theme : Theme = theme
        self.options : List[ImageTextPair] = options 

        self.selected = 0
        self.toggles = [False] * len(options)

        self.current_left = 0
        self.current_right = min(device.max_icons_for_large_grid_view,len(options))
     
    def _render(self):
        self.screen.clear()
        self.selected = max(0, self.selected)
        self.selected = min(len(self.options)-1, self.selected)
        
        if(self.selected < self.current_left):
            self.current_left -= 1
            self.current_right -=1

        if(self.selected >= self.current_right):
            self.current_left += 1
            self.current_right +=1

        visible_options: List[ImageTextPair] = self.options[self.current_left:self.current_right]

        for visible_index, imageTextPair in enumerate(visible_options):
            actual_index = self.current_left + visible_index
            imagePath = imageTextPair.get_image_path_selected() if actual_index == self.selected else imageTextPair.get_image_path()
            imageXOffset = self.device.large_grid_x_offset + visible_index * self.device.large_grid_spacing_multiplier
            self.screen.render_image(imagePath, 
                                     imageXOffset, 
                                     self.device.large_grid_y_offset)
            color = self.theme.text_color_selected if actual_index == self.selected else self.theme.text_color


            self.screen.render_text(imageTextPair.get_text().center(11), 
                                    imageXOffset,
                                    275, color, FontSize.SMALL)
            
        self.screen.present()

    def get_selection(self):
        self._render()
        running = True
        
        while running:
            if(self.controller.get_input()):
                if self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT:
                    self.selected-=1
                elif self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
                    self.selected+=1
                elif self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_A:
                    return self.options[self.selected]
                elif self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_B:
                    return ""

                self._render()
