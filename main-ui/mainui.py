import sdl2
import sdl2.ext
import time
from PIL import Image
import sdl2.sdlttf
from controller import Controller
from screen import Screen
from listview import ListView

ROM_DIR = "/mnt/sdcard/Roms/"

sdl2.ext.init(controller=True)


controller = Controller()
screen = Screen();

def run_option_toggle_ui():
    options = ["01234", "56789", "ABCDE" , "FGHIJ", "abcde", "fghij"]    
    options_list = ListView(screen,controller,options);
    selected = options_list.get_selection()
    print(f"{selected} was selected")
    selected = options_list.get_selection()
    print(f"{selected} was selected")

run_option_toggle_ui();
    

