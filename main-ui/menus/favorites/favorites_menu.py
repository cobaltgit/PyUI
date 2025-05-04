
import os
from pathlib import Path
import subprocess
from controller.controller import Controller
from controller.controller_inputs import ControllerInput
from devices.device import Device
from display.display import Display
from display.render_mode import RenderMode
from games.utils.favorite import Favorite
from menus.games.game_config_menu import GameConfigMenu
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.image_list_view import ImageListView
from views.selection import Selection


class FavoritesMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme

    def remove_extension(self,file_name):
        return os.path.splitext(file_name)[0]
    
    def get_image_path(self, rom_path):
        # Get the base filename without extension (e.g., "DKC")
        base_name = os.path.splitext(os.path.basename(rom_path))[0]
        
        # Get the parent directory of the ROM file
        parent_dir = os.path.dirname(rom_path)
        
        # Construct the path to the Imgs directory
        imgs_dir = os.path.join(parent_dir, "Imgs")
        
        # Construct the full path to the PNG image
        image_path = os.path.join(imgs_dir, base_name + ".png")
        if os.path.exists(image_path):
            return image_path
        else:
            return None
        
    def _is_favorite(self, favorites: list[Favorite], rom_file_path):
        return any(Path(rom_file_path).resolve() == Path(fav.rom_path).resolve() for fav in favorites)

    def _extract_game_system(self, rom_path):
        rom_path = os.path.abspath(os.path.normpath(rom_path))
        parts = os.path.normpath(rom_path).split(os.sep)
        try:
            roms_index = parts.index("Roms")
            return parts[roms_index + 1]
        except (ValueError, IndexError) as e:
            print(f"Error extracting subdirectory after 'Roms' for {rom_path}: {e}")
        return None  # "Roms" not found or no subdirectory after it
        
    def run_rom_selection(self) :
        selected = Selection(None,None,0)
        # Regenerate as part of while loop in case the options menu changes anything
        while(selected is not None):
            rom_list = []
            favorites = self.device.parse_favorites()
            for favorite in favorites:
                rom_file_name = os.path.basename(favorite.rom_path)
                img_path = self.get_image_path(favorite.rom_path)
                rom_list.append(
                    GridOrListEntry(
                        text=self.remove_extension(rom_file_name)  +" (" + self._extract_game_system(favorite.rom_path)+")",
                        image_path=img_path,
                        image_path_selected=img_path,
                        description="Favorite", 
                        icon=None,
                        value=favorite.rom_path)
                )

            img_offset_x = self.device.screen_width - 10
            img_offset_y = (self.device.screen_height - self.display.get_top_bar_height() + self.display.get_bottom_bar_height())//2 + self.display.get_top_bar_height() - self.display.get_bottom_bar_height()
            options_list = ImageListView(self.display,self.controller,self.device,self.theme, "Favorites",
                                        rom_list, img_offset_x, img_offset_y, self.theme.rom_image_width, self.theme.rom_image_height,
                                        selected.get_index(), ImageListView.SHOW_ICONS, RenderMode.MIDDLE_RIGHT_ALIGNED)
            selected = options_list.get_selection([ControllerInput.A, ControllerInput.X])
            if(selected is not None):
                if(ControllerInput.A == selected.get_input()):
                    self.device.run_game(selected.get_selection().get_value())
                    self.controller.clear_input_queue()
                elif(ControllerInput.X == selected.get_input()):
                    GameConfigMenu(self.display, self.controller, self.device, self.theme, self._extract_game_system(selected.get_selection().get_value()), selected.get_selection().get_value()).show_config()
