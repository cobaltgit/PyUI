import sdl2
import sdl2.ext
from controller.controller import Controller
from screen import Screen
from views.listview import ListView
from pathlib import Path
from themes.any_theme import AnyTheme

sdl2.ext.init(controller=True)

theme = AnyTheme("/mnt/sdcard/Themes/SPRUCE/") 
controller = Controller()
screen = Screen(theme);

def run_option_toggle_ui():
    roms_folders = [f.name for f in Path("/mnt/sdcard/Roms/").iterdir() if f.is_dir()]
    roms_folders.sort()
    options_list = ListView(screen,controller,roms_folders);
    selected = options_list.get_selection()
    print(f"{selected} was selected")

run_option_toggle_ui();
    

