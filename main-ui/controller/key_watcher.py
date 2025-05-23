
import os
import struct
import select
import time

from devices.device import Device




# Constants for Linux input
EVENT_FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)
EV_KEY = 0x01  # Event type for keyboard
KEY_PRESS = 1
KEY_REPEAT = 2


class KeyWatcher:

    def __init__(self, event_path):
        self.event_path = event_path


    def read_keyboard_input(self, timeout=1.0):
        """
        Polls for a single key event from a Linux input device (e.g., keyboard).

        Args:
            timeout (float): Time in seconds to wait before giving up.

        Returns:
            tuple or None: (keycode, is_down) where is_down is True for key press/repeat,
                        False for key release. Returns None on timeout or error.
        """
        try:
            fd = os.open(self.event_path, os.O_RDONLY | os.O_NONBLOCK)
        except OSError as e:
            print(f"Error opening {self.event_path}: {e}")
            return None

        try:
            rlist, _, _ = select.select([fd], [], [], timeout)
            if rlist:
                data = os.read(fd, EVENT_SIZE)
                if len(data) == EVENT_SIZE:
                    _, _, event_type, code, value = struct.unpack(EVENT_FORMAT, data)
                    if event_type == EV_KEY:
                        is_down = value in (KEY_PRESS, KEY_REPEAT)
                        return (code, is_down)
        except Exception as e:
            print(f"Error reading input: {e}")
        finally:
            os.close(fd)

        return (None,None)
    
    def poll_keyboard(self):
        last_recorded_time = 0
        while(True):
            code, is_key_down = self.read_keyboard_input()
            if(code is not None):
               if(time.time() - last_recorded_time > 0.1):
                    from controller.controller import Controller
                    controller_input = Device.map_key(code)
                    Controller.non_sdl_input_event(controller_input, is_key_down)
                    last_recorded_time = time.time()