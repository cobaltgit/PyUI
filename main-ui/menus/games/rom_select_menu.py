
import os
import subprocess
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from games.utils.game_system_utils import GameSystemUtils
from games.utils.rom_utils import RomUtils
from themes.theme import Theme
from views.listview import ListView


class RomSelectMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.rom_utils : RomUtils= RomUtils()

    def run_rom_selection(self,system) :
        selected = "new"
        options_list = ListView(self.display,self.controller,self.device,self.theme, self.rom_utils.get_roms(system))
        while((selected := options_list.get_selection()) is not None):
            print(f"{selected} was selected")
            subprocess.run(["/mnt/sdcard/Emu/.emu_setup/standard_launch.sh", 
                            os.path.join(self.rom_utils.get_roms_path(),system,selected)])
            self.controller.clear_input_queue()

