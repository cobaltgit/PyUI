import sdl2
import time

class ListView:
    def __init__(self, screen, controller, options):
        self.screen = screen
        self.controller = controller
        self.options = options
        self.selected = 0
        self.toggles = [False] * len(options)
        self.line_height = screen.get_line_height() + 10  # add 5px padding between lines

     
    def _render(self):
        self.screen.clear()
        self.selected = max(0, self.selected)
        self.selected = min(len(self.options)-1, self.selected)

        for i, (label, state) in enumerate(zip(self.options, self.toggles)):
            text = f"{label.ljust(5)} [{'y' if state else 'n'}]"
            if(i == self.selected) :
                self.screen.render_text(text, 50, 50 + i * self.line_height, color=(255, 255, 0))
            else :
                self.screen.render_text(text, 50, 50 + i * self.line_height, color=(255, 255, 255))
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
