from typing import List
from controller.controller_inputs import ControllerInput
from display.display import Display
import sdl2
from devices.device import Device
from controller.controller import Controller
from themes.theme import Theme

class ListView:

    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, options: List[str]):
        self.display = display
        self.controller = controller
        self.device = device
        self.theme = theme
        self.options = options

        self.selected = 0
        self.toggles = [False] * len(options)
        self.line_height = display.get_line_height() + 10  # add 5px padding between lines
        self.current_top = 0
        self.current_bottom = min(device.max_rows_for_list,len(options))
     
    def _render(self):
        self.display.clear()
        self.selected = max(0, self.selected)
        self.selected = min(len(self.options)-1, self.selected)
        
        while(self.selected < self.current_top):
            self.current_top -= 1
            self.current_bottom -=1

        while(self.selected >= self.current_bottom):
            self.current_top += 1
            self.current_bottom +=1

        visible_options = self.options[self.current_top:self.current_bottom]

        for visible_index, (label) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
            color = self.theme.text_color_selected if actual_index == self.selected else self.theme.text_color
            self.display.render_text(label, 50, 35 + visible_index * self.line_height, color=color)
            
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
