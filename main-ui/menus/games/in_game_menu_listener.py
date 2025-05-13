

import signal
import subprocess
import time
from controller.controller import Controller
from controller.controller_inputs import ControllerInput
from devices.device import Device
from display.display import Display
from menus.games.in_game_menu_popup import InGameMenuPopup
from themes.theme import Theme
from utils.logger import PyUiLogger
from views.view_creator import ViewCreator
import psutil
import signal

class InGameMenuListener:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.view_creator = ViewCreator(display,controller,device,theme)
        self.popup_menu = InGameMenuPopup(display,controller,device,theme)
            
    def send_signal(self, proc: subprocess.Popen, sig, timeout: float = 3.0):
        try:
            ps_proc = psutil.Process(proc.pid)

            # Send SIGTERM to all children
            children = ps_proc.children(recursive=True)
            for child in children:
                child.send_signal(sig)
            ps_proc.send_signal(sig)

            if(signal.SIGTERM == sig):
                # Wait up to `timeout` seconds
                deadline = time.time() + timeout
                while time.time() < deadline:
                    if not ps_proc.is_running() and all(not child.is_running() for child in children):
                        return  # All terminated gracefully
                    time.sleep(0.1)
            
                # If still running, force kill
                for child in children:
                    if child.is_running():
                        print(f"force killing child {child}")
                        child.kill()
                if ps_proc.is_running():
                    print(f"force killing ps_proc {ps_proc}")
                    ps_proc.kill()

        except Exception as e:
            print(f"Error in close_game: {e}")


    def game_launched(self, game_process: subprocess.Popen):
        while(game_process.poll() is None):
            if(self.controller.get_input()):
                if ControllerInput.MENU == self.controller.last_input():
                    self.send_signal(game_process, signal.SIGSTOP)
                    self.display.reinitialize()
                    continue_running = self.popup_menu.run_popup_menu_selection()
                    self.display.deinit_display()
                    if(continue_running):
                        game_process.send_signal(signal.SIGCONT)
                    else:
                        print(f"exit")
                        self.send_signal(game_process, signal.SIGCONT)
                        time.sleep(0.1)
                        self.send_signal(game_process, signal.SIGTERM)
        
        PyUiLogger.get_logger().debug(f"Game exit code was {game_process.poll()}")
