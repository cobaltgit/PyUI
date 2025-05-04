
import os
from pathlib import Path
import subprocess
from controller.controller import Controller
from controller.controller_inputs import ControllerInput
from devices.device import Device
from display.display import Display
from display.render_mode import RenderMode
from games.utils.favorite import Favorite
from games.utils.rom_utils import RomUtils
from menus.games.game_config_menu import GameConfigMenu
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.image_list_view import ImageListView
from views.selection import Selection


class RomSelectMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.roms_path = "/mnt/sdcard/Roms/"
        self.rom_utils : RomUtils= RomUtils(self.roms_path)

    def remove_extension(self,file_name):
        return os.path.splitext(file_name)[0]
    
    def get_image_path(self,imgs_dir, file_name):
        img_file = os.path.join(imgs_dir ,self.remove_extension(file_name)+".png")
        if os.path.exists(img_file):
            return img_file
        else:
            return None
        
    def _is_favorite(self, favorites: list[Favorite], rom_file_path):
        return any(Path(rom_file_path).resolve() == Path(fav.rom_path).resolve() for fav in favorites)

    def run_rom_selection(self,game_system) :
        imgs_dir = os.path.join(self.roms_path, game_system,"Imgs")

        selected = Selection(None,None,0)
        rom_list = []
        
        favorites = self.device.parse_favorites()
        for rom_file_path in self.rom_utils.get_roms(game_system):
            rom_file_name = os.path.basename(rom_file_path)
            img_path = self.get_image_path(imgs_dir,rom_file_name)
            icon=self.theme.favorite_icon if self._is_favorite(favorites, rom_file_path) else None
            rom_list.append(
                GridOrListEntry(
                    text=self.remove_extension(rom_file_name),
                    image_path=img_path,
                    image_path_selected=img_path,
                    description=game_system, 
                    icon=icon,
                    value=rom_file_name)
            )

        img_offset_x = self.device.screen_width - 10
        img_offset_y = (self.device.screen_height - self.display.get_top_bar_height())//2 + self.display.get_top_bar_height()
        options_list = ImageListView(self.display,self.controller,self.device,self.theme, game_system,
                                     rom_list, img_offset_x, img_offset_y, self.theme.rom_image_width, self.theme.rom_image_height,
                                     selected.get_index(), ImageListView.SHOW_ICONS, RenderMode.MIDDLE_RIGHT_ALIGNED)
        while((selected := options_list.get_selection([ControllerInput.A, ControllerInput.X])) is not None):
            if(ControllerInput.A == selected.get_input()):
                self.device.run_game(os.path.join(self.roms_path,game_system,selected.get_selection().get_value()))
                self.controller.clear_input_queue()
            elif(ControllerInput.X == selected.get_input()):
                GameConfigMenu(self.display, self.controller, self.device, self.theme, game_system, selected.get_selection().get_value()).show_config()
