
import os
from controller.controller_inputs import ControllerInput
from devices.device import Device
from display.on_screen_keyboard import OnScreenKeyboard
from menus.settings import settings_menu
from menus.settings.display_settings_menu import DisplaySettingsMenu
from menus.settings.timezone_menu import TimezoneMenu
from utils.logger import PyUiLogger
from utils.py_ui_config import PyUiConfig
from views.grid_or_list_entry import GridOrListEntry


class ExtraSettingsMenu(settings_menu.SettingsMenu):
    def __init__(self):
        super().__init__()
        self.on_screen_keyboard = OnScreenKeyboard()

    def reboot(self, input: ControllerInput):
        if(ControllerInput.A == input):
            Device.run_app(Device.reboot_cmd())


    def launch_display_settings(self,input):
        if(ControllerInput.A == input):
            DisplaySettingsMenu().show_menu()

    def launch_stock_os_menu(self,input):
        if(ControllerInput.A == input):
            Device.launch_stock_os_menu()

    def calibrate_sticks(self,input):
        if(ControllerInput.A == input):
            Device.calibrate_sticks()

    def set_timezone(self,input):
        if(ControllerInput.A == input):
            tz = TimezoneMenu().ask_user_for_timezone()
            if(tz is not None):
                PyUiConfig.set_timezone(tz)


    def build_options_list(self):
        option_list = []
        
        option_list.append(
                GridOrListEntry(
                        primary_text="Display Settings",
                        value_text=None,
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.launch_display_settings
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Set Timezone",
                        value_text=None,
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.set_timezone
                    )
            )
                    
        option_list.append(
                GridOrListEntry(
                        primary_text="Calibrate Analog Sticks",
                        value_text=None,
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.calibrate_sticks
                    )
            )

        option_list.append(
                GridOrListEntry(
                        primary_text="Reboot",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.reboot
                )
        )
            
        option_list.append(
                GridOrListEntry(
                        primary_text="Stock OS Menu",
                        value_text=None,
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.launch_stock_os_menu
                    )
            )
                    

            
        
        return option_list
