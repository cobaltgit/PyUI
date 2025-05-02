from abc import ABC, abstractmethod

from controller.controller import Controller
from controller.controller_inputs import ControllerInput


class ListView(ABC):
    def __init__(self, controller: Controller):
        self.controller = controller
        self.current_top = 0
        self.current_bottom = 0

    @abstractmethod
    def _render(self):
        pass
    
    def get_selection(self):
        self._render_common()
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

                self._render_common()

    def _render_common(self):
        self.display.clear(self.top_bar_text)
        self.selected = max(0, self.selected)
        self.selected = min(len(self.options)-1, self.selected)
        
        while(self.selected < self.current_top):
            self.current_top -= 1
            self.current_bottom -=1

        while(self.selected >= self.current_bottom):
            self.current_top += 1
            self.current_bottom +=1

        self._render()

    def adjust_selected(self, amount):
        if(amount < 0):
            if(self.current_top + amount < 0):
                amount = -1 * self.selected
        elif(self.current_bottom - amount > len(self.options)):
                amount = self.current_bottom - self.selected

        self.selected += amount
        self.current_top += amount
        self.current_bottom += amount
