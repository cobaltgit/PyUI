import sdl2
import sdl2.ext
from controller.controller import Controller
from screen.screen import Screen
from games.utils.game_system_utils import GameSystemUtils
from views.image_text_pair import ImageTextPair
from views.large_grid_view import LargeGridView
from views.listview import ListView
from themes.theme import Theme
from devices.miyoo_flip import MiyooFlip

sdl2.ext.init(controller=True)

device = MiyooFlip()

theme = Theme("/mnt/sdcard/Themes/SPRUCE/") 
controller = Controller()
screen = Screen(theme, device)
game_utils = GameSystemUtils()


def run_system_selection() :
    options_list = ListView(screen,controller,device,theme, game_utils.get_active_systems())
    selected = options_list.get_selection()
    print(f"{selected} was selected")

def run_main_menu_selection():
    image_text_list = [
        ImageTextPair(theme.favorite, theme.favorite_selected, "Favorite"),
        ImageTextPair(theme.game,theme.game_selected, "Game"),
        ImageTextPair(theme.app,theme.app_selected, "App"),
        ImageTextPair(theme.settings,theme.settings_selected, "Setting")
    ]

    options_list = LargeGridView(screen,controller,device,theme, image_text_list)
    selected = options_list.get_selection()
    print(f"{selected.get_text()} was selected")
    if(selected.get_text() == "Game"):
        run_system_selection()

run_main_menu_selection()
    

