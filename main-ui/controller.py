import sdl2
import ctypes
from ctypes import byref


class Controller:
    def __init__(self):
        self.controller = None
        self.index = None
        self.name = None
        self.mapping = None
        self._init_controller()
        self.event = sdl2.SDL_Event()


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
            
    def get_input(self):
        sdl2.SDL_PollEvent(byref(self.event))
        return self.last_event_was_controller()
    
    def last_event_was_controller(self):
        return self._last_event().type == sdl2.SDL_CONTROLLERBUTTONDOWN

    def _last_event(self):
        return self.event
        
    def last_input(self):
        return self.event.cbutton.button