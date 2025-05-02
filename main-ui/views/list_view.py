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
                    self.adjust_selected(-1)
                elif self.controller.last_input() == ControllerInput.DPAD_DOWN:
                    self.adjust_selected(1)
                elif self.controller.last_input() == ControllerInput.L1:
                    self.adjust_selected(-1*self.max_rows+1)
                elif self.controller.last_input() == ControllerInput.R1:
                    self.adjust_selected(self.max_rows-1)
                elif self.controller.last_input() == ControllerInput.A:
                    return self.options[self.selected]
                elif self.controller.last_input() == ControllerInput.B:
                    return None

                self._render_common()

    def _render_common(self):
        self.display.clear(self.top_bar_text)

        self._render()

    def adjust_selected_top_bottom_for_overflow(self):
        self.selected = max(0, self.selected)
        self.selected = min(len(self.options)-1, self.selected)
        
        while(self.selected < self.current_top):
            self.current_top -= 1
            self.current_bottom -=1

        while(self.selected >= self.current_bottom):
            self.current_top += 1
            self.current_bottom +=1


    def adjust_selected(self, amount):
        if(self.selected == 0 and amount < 0):
            # Hitting up when on the top most row
            delta = self.current_bottom - self.current_top
            self.selected = len(self.options)-1
            self.current_bottom = len(self.options)-1
            self.current_top = max(0, self.current_bottom - delta)
        elif(self.selected == len(self.options)-1 and amount > 0):
            # Hitting down when on the bottom most row
            delta = self.current_bottom - self.current_top
            self.selected = 0
            self.current_top = 0
            self.current_bottom = min(delta, len(self.options)-1)
        else :    
            # Normal adjustment
            self.selected += amount
            if(amount > 1):
                self.current_top += amount
                self.current_bottom += amount

        # TODO rework above logic to not need this (though minor cost to leaving it)
        self.adjust_selected_top_bottom_for_overflow()