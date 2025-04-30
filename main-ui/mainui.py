import sdl2
import sdl2.ext
from controller.controller import Controller
from screen.screen import Screen
from games.utils.game_system_utils import GameSystemUtils
from views.listview import ListView
from themes.theme import Theme
from devices.miyoo_flip import MiyooFlip

sdl2.ext.init(controller=True)

device = MiyooFlip()

theme = Theme("/mnt/sdcard/Themes/SPRUCE/") 
controller = Controller()
screen = Screen(theme, device)
game_utils = GameSystemUtils()

def run_option_toggle_ui():
    options_list = ListView(screen,controller,device, game_utils.get_active_systems())
    selected = options_list.get_selection()
    print(f"{selected} was selected")

run_option_toggle_ui()
    

