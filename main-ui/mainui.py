import sdl2
import sdl2.ext

from menus.main_menu import MainMenu
from controller.controller import Controller
from display.display import Display
from themes.theme import Theme
from devices.miyoo_flip import MiyooFlip

theme = Theme("/mnt/sdcard/Themes/SPRUCE/") 
device = MiyooFlip()
display = Display(theme, device)
controller = Controller(device)

main_menu = MainMenu(display, controller, device, theme)

main_menu.run_main_menu_selection()
    
theme.set_theme_path("/mnt/sdcard/Themes/HeyDW's Blue/") 

main_menu.run_main_menu_selection()


