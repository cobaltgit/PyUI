
import os
import subprocess
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from games.utils.rom_utils import RomUtils
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.image_list_view import ImageListView


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
        
    def run_rom_selection(self,system) :
        imgs_dir = os.path.join(self.roms_path, system,"Imgs")

        selected = "new"
        rom_list = []
        
        for rom in self.rom_utils.get_roms(system):
            img_path = self.get_image_path(imgs_dir,rom)
            rom_list.append(
                GridOrListEntry(
                    self.remove_extension(rom),
                    img_path,
                    value=rom
                )
            )

        img_offset_x = int(3/4*self.device.screen_width)
        img_offset_y = int(self.device.screen_height/5)
        options_list = ImageListView(self.display,self.controller,self.device,self.theme, system,
                                     rom_list, img_offset_x, img_offset_y)
        while((selected := options_list.get_selection()) is not None):
            self.device.run_game(os.path.join(self.roms_path,system,selected.get_value()))
            self.controller.clear_input_queue()

