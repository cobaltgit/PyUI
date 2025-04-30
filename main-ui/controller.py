import sdl2


class ControllerManager:
    def __init__(self):
        self.controller = None
        self.index = None
        self.name = None
        self.mapping = None
        self._init_controller()

    def _init_controller(self):
        print("Checking for a controller")
        count = sdl2.SDL_NumJoysticks()
        for index in range(count):
            print(f"Checking index {index}")
            if sdl2.SDL_IsGameController(index):
                controller = sdl2.SDL_GameControllerOpen(index)
                if controller:
                    self.controller = controller
                    self.index = index
                    self.name = sdl2.SDL_GameControllerName(controller).decode()
                    self.mapping = sdl2.SDL_GameControllerMapping(controller).decode()
                    print(f"Opened GameController {index}: {self.name}")
                    print(f" {self.mapping}")
                    return
        print("No game controller found.")

    def get_controller(self):
        return self.controller

    def close(self):
        if self.controller:
            sdl2.SDL_GameControllerClose(self.controller)
            self.controller = None
