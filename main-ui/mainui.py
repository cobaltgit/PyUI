from games.utils.rom_utils import RomUtils
import sdl2
import sdl2.ext
from controller.controller import Controller
from display.display import Display
from games.utils.game_system_utils import GameSystemUtils
from views.image_text_pair import ImageTextPair
from views.large_grid_view import LargeGridView
from views.listview import ListView
from themes.theme import Theme
from devices.miyoo_flip import MiyooFlip
import subprocess
import os

sdl2.ext.init(controller=True)
sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_GAMECONTROLLER)

device = MiyooFlip()

theme = Theme("/mnt/sdcard/Themes/SPRUCE/") 
controller = Controller()
display = Display(theme, device)
game_utils = GameSystemUtils()
rom_utils = RomUtils()


def run_rom_selection(system) :
    selected = "new"
    options_list = ListView(display,controller,device,theme, rom_utils.get_roms(system))
    while((selected := options_list.get_selection()) is not None):
        print(f"{selected} was selected")
        subprocess.run(["/mnt/sdcard/Emu/.emu_setup/standard_launch.sh", 
                        os.path.join(rom_utils.get_roms_path(),system,selected)])
        controller.clear_input_queue()

def run_system_selection() :
    selected = "new"
    options_list = ListView(display,controller,device,theme, game_utils.get_active_systems())
    while((selected := options_list.get_selection()) is not None):
        print(f"{selected} was selected")
        run_rom_selection(selected)

def run_main_menu_selection():
    image_text_list = [
        ImageTextPair(theme.favorite, theme.favorite_selected, "Favorite"),
        ImageTextPair(theme.game,theme.game_selected, "Game"),
        ImageTextPair(theme.app,theme.app_selected, "App"),
        ImageTextPair(theme.settings,theme.settings_selected, "Setting")
    ]

    options_list = LargeGridView(display,controller,device,theme, image_text_list)
    selected = "new"
    while((selected := options_list.get_selection()) is not None):        
        print(f"{selected.get_text()} was selected")
        if(selected.get_text() == "Game"):
            run_system_selection()

run_main_menu_selection()
    

