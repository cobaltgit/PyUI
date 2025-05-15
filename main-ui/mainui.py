import argparse
from multiprocessing import get_logger
import os
import sys
import threading
from controller.key_watcher import KeyWatcher
from devices.trimui.trim_ui_brick import TrimUIBrick
import sdl2
import sdl2.ext

from menus.main_menu import MainMenu
from controller.controller import Controller
from display.display import Display
from themes.theme import Theme
from devices.miyoo_flip import MiyooFlip
from utils.logger import PyUiLogger
from utils.py_ui_config import PyUiConfig



print("Arguments:", sys.argv)
print("Script name:", sys.argv[0])

parser = argparse.ArgumentParser()

parser.add_argument('-logDir', type=str, default='/mnt/SDCARD/pyui/logs/', help='Directory to store logs')
parser.add_argument('-pyUiConfig', type=str, default='/mnt/SDCARD/Saves/pyui-config.json', help='Location of PyUI config')

args = parser.parse_args()

print("logDir:", args.logDir)

    
PyUiLogger.init(args.logDir, "PyUI")

num = sdl2.SDL_GetNumRenderDrivers()
for i in range(num):
    info = sdl2.SDL_RendererInfo()
    sdl2.SDL_GetRenderDriverInfo(i, info)
    print(f"Found Renderer {i}: {info.name.decode()}")

config = PyUiConfig(args.pyUiConfig)
config.load()

selected_theme = os.path.join(config["themeDir"],config["theme"])
                              
PyUiLogger.get_logger().info(f"{selected_theme}")


if os.path.exists("/userdata/system.json"):
    device = MiyooFlip()
elif os.path.exists("/mnt/UDISK/system.json"):
    device = TrimUIBrick()

theme = Theme(os.path.join(config["themeDir"],config["theme"]), device.screen_width, device.screen_height)

display = Display(theme, device)
controller = Controller(device, config)

main_menu = MainMenu(display, controller, device, theme, config)

startup_thread = threading.Thread(target=device.perform_startup_tasks())
startup_thread.start()

key_watcher = KeyWatcher(device)
key_polling_thread = threading.Thread(target=key_watcher.poll_keyboard, daemon=True)
key_polling_thread.start()


main_menu.run_main_menu_selection()
os._exit(0)