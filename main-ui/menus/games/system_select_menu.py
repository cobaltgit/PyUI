
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from games.utils.game_system_utils import GameSystemUtils
from menus.games.rom_select_menu import RomSelectMenu
from themes.theme import Theme
from views.listview import ListView


class SystemSelectMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.game_utils : GameSystemUtils = GameSystemUtils()
        self.rom_select_menu : RomSelectMenu = RomSelectMenu(display,controller,device,theme)

    def run_system_selection(self) :
        selected = "new"
        options_list = ListView(self.display,self.controller,self.device,self.theme, self.game_utils.get_active_systems())
        while((selected := options_list.get_selection()) is not None):
            print(f"{selected} was selected")
            self.rom_select_menu.run_rom_selection(selected)
