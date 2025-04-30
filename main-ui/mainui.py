import sdl2
import sdl2.ext
import time
from PIL import Image
import sdl2.sdlttf
from controller import Controller
from screen import Screen
from listview import ListView
from pathlib import Path

sdl2.ext.init(controller=True)


controller = Controller()
screen = Screen();

def run_option_toggle_ui():
    roms_folders = [f.name for f in Path("/mnt/sdcard/Roms/").iterdir() if f.is_dir()]
    options_list = ListView(screen,controller,roms_folders);
    selected = options_list.get_selection()
    print(f"{selected} was selected")

run_option_toggle_ui();
    

