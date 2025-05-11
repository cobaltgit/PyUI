
import os
from controller.controller import Controller
from controller.controller_inputs import ControllerInput
from devices.device import Device
from display.display import Display
from display.on_screen_keyboard import OnScreenKeyboard
from menus.settings import settings_menu
from menus.settings.bluetooth_menu import BluetoothMenu
from menus.settings.wifi_menu import WifiMenu
from themes.theme import Theme
from utils.py_ui_config import PyUiConfig
from views.descriptive_list_view import DescriptiveListView
from views.grid_or_list_entry import GridOrListEntry
from views.selection import Selection
from views.view_creator import ViewCreator
from views.view_type import ViewType


class AdvanceSettingsMenu(settings_menu.SettingsMenu):
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, config: PyUiConfig):
        super().__init__(
            display=display,
            controller=controller,
            device=device,
            theme=theme,
            config=config)
        self.on_screen_keyboard = OnScreenKeyboard(display,controller,device,theme)

    def reboot(self, input: ControllerInput):
        if(ControllerInput.A == input):
            self.device.run_app(self.device.reboot_cmd)
    
    
    def brightness_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.L1 == input):
            self.device.lower_brightness()
        elif(ControllerInput.DPAD_RIGHT == input or ControllerInput.R1 == input):
            self.device.raise_brightness()

    def contrast_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.L1 == input):
            self.device.lower_contrast()
        elif(ControllerInput.DPAD_RIGHT == input or ControllerInput.R1 == input):
            self.device.raise_contrast()

    def saturation_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.L1 == input):
            self.device.lower_saturation()
        elif(ControllerInput.DPAD_RIGHT == input or ControllerInput.R1 == input):
            self.device.raise_saturation()
    

    def show_on_screen_keyboard(self, input):
        print(self.on_screen_keyboard.get_input("On Screen Keyboard Test"))


    def build_options_list(self):
        option_list = []

        option_list.append(
                GridOrListEntry(
                        primary_text="Brightness",
                        value_text="<    " + str(self.device.brightness) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.brightness_adjust
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Contrast",
                        value_text="<    " + str(self.device.contrast) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.contrast_adjust
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Saturation",
                        value_text="<    " + str(self.device.saturation) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.saturation_adjust
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="On Screen Keyboard",
                        value_text=None,
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.show_on_screen_keyboard
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
        
        return option_list
