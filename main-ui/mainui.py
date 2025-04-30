import sdl2
import sdl2.ext

from games.utils.rom_utils import RomUtils
from menus.main_menu import MainMenu
from controller.controller import Controller
from display.display import Display
from themes.theme import Theme
from devices.miyoo_flip import MiyooFlip

sdl2.ext.init(controller=True)
sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_GAMECONTROLLER)

device = MiyooFlip()

theme = Theme("/mnt/sdcard/Themes/SPRUCE/") 
controller = Controller()
display = Display(theme, device)
main_menu = MainMenu(display, controller, device, theme)

main_menu.run_main_menu_selection()
    

