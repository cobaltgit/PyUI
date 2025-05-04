
import os
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from themes.theme import Theme
from views.descriptive_list_view import DescriptiveListView
from views.grid_or_list_entry import GridOrListEntry
from views.selection import Selection


class SettingsMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display = display
        self.controller = controller
        self.device = device
        self.theme = theme
    
    def shutdown(self):
       self.device.run_app(self.device.power_off_cmd)
    
    def reboot(self):
        self.device.run_app(self.device.power_off_cmd)

    def show_menu(self) :
        selected = Selection(None, None, 0)

        while(selected is not None):
            option_list = []
            option_list.append(
                GridOrListEntry(
                        text="Power Off",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.shutdown
                    )
            )
            option_list.append(
                GridOrListEntry(
                        text="Reboot",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.reboot
                    )
            )
            option_list = DescriptiveListView(self.display,self.controller,self.device,self.theme, 
                                              "Settings", option_list, self.theme.get_list_small_selected_bg(),
                                              selected.get_index())
            selected = option_list.get_selection()

            if(selected is not None):
                selected.get_selection().get_value()()
