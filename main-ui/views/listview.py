from typing import List
from screen.screen import Screen
import sdl2
from devices.device import Device
from controller.controller import Controller

class ListView:

    def __init__(self, screen: Screen, controller: Controller, device: Device, options: List[str]):
        self.screen = screen
        self.controller = controller
        self.options = options
        self.device = device
        self.selected = 0
        self.toggles = [False] * len(options)
        self.line_height = screen.get_line_height() + 10  # add 5px padding between lines
        self.current_top = 0
        self.current_bottom = min(device.max_rows_for_list,len(options))
     
    def _render(self):
        self.screen.clear()
        self.selected = max(0, self.selected)
        self.selected = min(len(self.options)-1, self.selected)
        
        if(self.selected < self.current_top):
            self.current_top -= 1
            self.current_bottom -=1;

        if(self.selected >= self.current_bottom):
            self.current_top += 1
            self.current_bottom +=1;

        print(f"self.current_top is {self.current_top}")
        print(f"self.current_bottom is {self.current_bottom}")

        visible_options = list(zip(self.options, self.toggles))[self.current_top:self.current_bottom]

        for visible_index, (label, state) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
            color = (255, 255, 0) if actual_index == self.selected else (255, 255, 255)
            self.screen.render_text(label, 50, 50 + visible_index * self.line_height, color=color)
            
        self.screen.present()

    def get_selection(self):
        self._render()
        running = True
        
        while running:
            if(self.controller.get_input()):
                if self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP:
                    self.selected-=1
                elif self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN:
                    self.selected+=1
                elif self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT:
                    print("⬅️ Left")
                elif self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
                    print("➡️ Right")
                elif self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_A:
                    return self.options[self.selected]
                elif self.controller.last_input() == sdl2.SDL_CONTROLLER_BUTTON_START:
                    print("➡️ Start")

                self._render()
