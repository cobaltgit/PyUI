
import os
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from menus.games.game_system_config import GameSystemConfig
from themes.theme import Theme
from views.descriptive_list_view import DescriptiveListView
from views.grid_or_list_entry import GridOrListEntry


# Would like this to be generic in the future but this is so Miyoo specific right now 
# Due to the oddities in how its handled
class GameConfigMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, game_system: str, game : str):
        self.display = display
        self.controller = controller
        self.device = device
        self.theme = theme
        self.game_system = game_system
        self.game = game
    


    def show_config(self) :
        selected = "new"
        #Loop is weird here due to how these options are handled.
        # We essentially need to re-read the game system config every time
        # an option is selected
        while(selected is not None):
            game_system_config = GameSystemConfig(self.game_system)

            config_list = []
            for config_option in game_system_config.get_launchlist():
                config_list.append(
                    GridOrListEntry(
                        text=config_option.get('name'),
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=config_option.get('launch')
                    )
                )
                        

            config_list = DescriptiveListView(self.display,self.controller,self.device,self.theme, 
                                              self.game_system + " Configuration", config_list, self.theme.get_game_config_list_selected_bg())
            selected = config_list.get_selection()

            if(selected is not None):
                # Miyoo handles this strangley
                # Example rom /mnt/sdcard/Roms/PORTS/PokeMMO.sh               
                # example arg /media/sdcard0/Emu/PORTS/../../Roms/PORTS/PokeMMO.sh
                #/media/sdcard0/Emu/PORTS/../../Roms/PORTS/PokeMMO.sh
                miyoo_game_path = os.path.join("/media/sdcard0/Emu", self.game_system, "../../Roms", self.game_system, self.game)
                self.device.run_app([selected.get_selection().get_value(), miyoo_game_path])
                self.display.reinitialize()
