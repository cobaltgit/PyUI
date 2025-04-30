import sdl2
import sdl2.ext
from controller.controller import Controller
from screen import Screen
from games.utils.game_system_utils import GameSystemUtils
from views.listview import ListView
from themes.any_theme import AnyTheme

sdl2.ext.init(controller=True)

theme = AnyTheme("/mnt/sdcard/Themes/SPRUCE/") 
controller = Controller()
screen = Screen(theme)
game_utils = GameSystemUtils()

def run_option_toggle_ui():
    options_list = ListView(screen,controller,game_utils.get_active_systems())
    selected = options_list.get_selection()
    print(f"{selected} was selected")

run_option_toggle_ui()
    

