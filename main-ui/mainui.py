import argparse
import os
import sys
import threading
from devices.device import Device
from devices.trimui.trim_ui_brick import TrimUIBrick
from menus.games.utils.favorites_manager import FavoritesManager
from menus.games.utils.recents_manager import RecentsManager
import sdl2
import sdl2.ext

from menus.main_menu import MainMenu
from controller.controller import Controller
from display.display import Display
from themes.theme import Theme
from devices.miyoo_flip import MiyooFlip
from utils.logger import PyUiLogger
from utils.py_ui_config import PyUiConfig



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-logDir', type=str, default='/mnt/SDCARD/pyui/logs/', help='Directory to store logs')
    parser.add_argument('-pyUiConfig', type=str, default='/mnt/SDCARD/Saves/pyui-config.json', help='Location of PyUI config')
    return parser.parse_args()

def log_renderer_info():
    num = sdl2.SDL_GetNumRenderDrivers()
    for i in range(num):
        info = sdl2.SDL_RendererInfo()
        sdl2.SDL_GetRenderDriverInfo(i, info)
        print(f"Found Renderer {i}: {info.name.decode()}")

def initialize_device():
    if os.path.exists("/userdata/system.json"):
        Device.init(MiyooFlip())
    elif os.path.exists("/mnt/UDISK/system.json"):
        Device.init(TrimUIBrick())
    else:
        raise RuntimeError("No supported device config found")


def background_startup():
    FavoritesManager.initialize(Device.get_favorites_path())
    RecentsManager.initialize(Device.get_recents_path())

def start_background_threads():
    startup_thread = threading.Thread(target=Device.perform_startup_tasks)
    startup_thread.start()

    # Background favorites/recents init thread
    background_thread = threading.Thread(target=background_startup)
    background_thread.start()

def main():
    args = parse_arguments()

    print("Arguments:", sys.argv)
    print("logDir:", args.logDir)

    PyUiLogger.init(args.logDir, "PyUI")

    log_renderer_info()

    PyUiConfig.init(args.pyUiConfig)

    selected_theme = os.path.join(PyUiConfig.get("themeDir"), PyUiConfig.get("theme"))
    PyUiLogger.get_logger().info(f"{selected_theme}")

    initialize_device()

    Theme.init(selected_theme, Device.screen_width(), Device.screen_height())
    Display.init()
    Controller.init()
    main_menu = MainMenu()

    start_background_threads()

    main_menu.run_main_menu_selection()

if __name__ == "__main__":
    main()
    os._exit(0)
