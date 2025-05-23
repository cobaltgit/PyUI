import time
from controller.controller_inputs import ControllerInput
from devices.device import Device
import sdl2
import ctypes
from ctypes import byref
import time

from utils.logger import PyUiLogger
from utils.py_ui_config import PyUiConfig

class Controller:
    controller = None
    index = None
    name = None
    mapping = None
    event = sdl2.SDL_Event()
    last_input_time = 0
    hold_delay = 0
    additional_button_watchers = []

    @staticmethod
    def init():
        Controller.clear_input_queue()
        Controller.init_controller()

    @staticmethod
    def init_controller():
        SDL_ENABLE = 1
        SDL_INIT_GAMECONTROLLER = 0x00002000

        sdl2.SDL_GameControllerEventState(SDL_ENABLE)
        sdl2.SDL_InitSubSystem(SDL_INIT_GAMECONTROLLER)
        PyUiLogger.get_logger().info("Checking for a controller")
        count = sdl2.SDL_NumJoysticks()
        for index in range(count):
            PyUiLogger.get_logger().info(f"Checking index {index}")
            if sdl2.SDL_IsGameController(index):
                controller = sdl2.SDL_GameControllerOpen(index)
                if controller:
                    Controller.controller = controller
                    Controller.index = index
                    Controller.name = sdl2.SDL_GameControllerName(controller).decode()
                    Controller.mapping = sdl2.SDL_GameControllerMapping(controller).decode()
                    PyUiLogger.get_logger().info(f"Opened GameController {index}: {Controller.name}")
                    PyUiLogger.get_logger().info(f" {Controller.mapping}")


    @staticmethod
    def re_init_controller():
        sdl2.SDL_QuitSubSystem(sdl2.SDL_INIT_GAMECONTROLLER)
        time.sleep(0.2)
        sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_GAMECONTROLLER)
        # 5. Pump events to make SDL notice new controllers
        for _ in range(10):
            sdl2.SDL_PumpEvents()
            time.sleep(0.1)
        Controller.init_controller()

    @staticmethod
    def new_bt_device_paired():
        Controller.re_init_controller()

    @staticmethod
    def get_controller():
        return Controller.controller

    @staticmethod
    def close():
        if Controller.controller:
            sdl2.SDL_GameControllerClose(Controller.controller)
            Controller.controller = None

    @staticmethod
    def still_held_down():
        #PyUiLogger.get_logger().debug(f"Checking if {Controller.last_input()} is still held down")
        return sdl2.SDL_GameControllerGetButton(Controller.controller, Controller.event.cbutton.button)

    @staticmethod
    def get_input(timeout=-2, is_check_for_hotkey=False):
        DEFAULT_TIMEOUT_FLAG = -2
        INPUT_DEBOUNCE_SECONDS = 0.2
        POLL_INTERVAL_SECONDS = 0.005

        if timeout == DEFAULT_TIMEOUT_FLAG:
            timeout = Device.input_timeout_default()

        now = time.time()
        time_since_last_input = now - Controller.last_input_time

        # Clear stale events if enough time has passed
        if time_since_last_input > INPUT_DEBOUNCE_SECONDS:
            sdl2.SDL_PumpEvents()
            Controller.clear_input_queue()

        sdl2.SDL_PumpEvents()
        start_time = time.time()

        # Wait if the input is being held down (anti-repeat logic)
        while Controller.still_held_down() and (time.time() - start_time < Controller.hold_delay):
            sdl2.SDL_PumpEvents()
            time.sleep(POLL_INTERVAL_SECONDS)

        was_hotkey = False
        if not Controller.still_held_down():
            # Reset hold delay and clear any lingering event
            Controller.hold_delay = PyUiConfig.get_turbo_delay_ms()
            Controller._last_event().type = 0

            # Blocking wait for event until timeout
            while True:
                elapsed = time.time() - start_time
                remaining_time = timeout - elapsed
                if remaining_time <= 0:
                    break

                ms_remaining = int(remaining_time * 1000)
                event_available = sdl2.SDL_WaitEventTimeout(byref(Controller.event), ms_remaining)

                if event_available:
                    last_input = Controller.last_input()

                    if last_input is not None:
                        if last_input == ControllerInput.MENU:
                            if not is_check_for_hotkey and not Controller.check_for_hotkey():
                                break  # Treat MENU as valid input
                            else:
                                was_hotkey = True
                                while Controller.still_held_down():
                                    Controller.check_for_hotkey()
                        else:
                            break  # Valid non-hotkey input

                    elif Controller._last_event().type == sdl2.SDL_CONTROLLERDEVICEADDED:
                        PyUiLogger.get_logger().info("New controller detected")
                        Controller.init_controller()
        elif(ControllerInput.MENU == Controller.last_input()):
            was_hotkey = True
            Controller.check_for_hotkey()
        else:
            Controller.hold_delay = 0.0  # No input was released yet

        Controller.last_input_time = time.time()
        return Controller.last_event_was_controller() and not was_hotkey

    @staticmethod
    def clear_input_queue():
        count = 0
        while count < 50:
            sdl2.SDL_PollEvent(byref(Controller.event))
            if Controller.event.cbutton.button == 0:
                count += 1
            else:
                count = 0

    @staticmethod
    def last_event_was_controller():
        return Controller._last_event().type in (
            sdl2.SDL_CONTROLLERBUTTONDOWN,
            sdl2.SDL_CONTROLLERAXISMOTION
        )

    @staticmethod
    def _last_event():
        return Controller.event

    @staticmethod
    def last_input():
        event = Controller._last_event()
        if event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
            return Device.map_digital_input(event.cbutton.button)
        elif event.type == sdl2.SDL_CONTROLLERAXISMOTION:
            return Device.map_analog_input(event.caxis.axis, event.caxis.value)
        return None

    @staticmethod
    def get_left_analog_x():
        sdl2.SDL_PumpEvents()
        return sdl2.SDL_GameControllerGetAxis(Controller.controller, sdl2.SDL_CONTROLLER_AXIS_LEFTX)

    @staticmethod
    def get_left_analog_y():
        sdl2.SDL_PumpEvents()
        return sdl2.SDL_GameControllerGetAxis(Controller.controller, sdl2.SDL_CONTROLLER_AXIS_LEFTY)

    @staticmethod
    def get_right_analog_x():
        sdl2.SDL_PumpEvents()
        return sdl2.SDL_GameControllerGetAxis(Controller.controller, sdl2.SDL_CONTROLLER_AXIS_RIGHTX)

    @staticmethod
    def get_right_analog_y():
        sdl2.SDL_PumpEvents()
        return sdl2.SDL_GameControllerGetAxis(Controller.controller, sdl2.SDL_CONTROLLER_AXIS_RIGHTY)

    @staticmethod 
    def add_button_watcher(button_watcher):
        Controller.additional_button_watchers.append(button_watcher)

    #return TRUE if it was a hotkey press, FALSE otherwise
    @staticmethod
    def check_for_hotkey():
        cached_event = Controller.event
        Controller.event = sdl2.SDL_Event()
        Controller._last_event().type = -1
        if(Controller.get_input(timeout=0.3,is_check_for_hotkey=True)):
            PyUiLogger.get_logger().info(f"Dected hotkey Menu + {Controller.last_input()}")
            time.sleep(0.3)
            Controller.event = cached_event
            return True # was
        else:
            Controller.event = cached_event
            return False
        
    @staticmethod
    def non_sdl_input_event(controller_input, is_down):
        if(is_down):
            Device.special_input(controller_input)