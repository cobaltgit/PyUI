
import os
from controller.controller import Controller
from controller.controller_inputs import ControllerInput
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
    
    def shutdown(self, input: ControllerInput):
        if(ControllerInput.A == input):
           self.device.run_app(self.device.power_off_cmd)
    
    def reboot(self, input: ControllerInput):
        if(ControllerInput.A == input):
            self.device.run_app(self.device.power_off_cmd)
    
    def brightness_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input):
            self.device.lower_brightness()
        elif(ControllerInput.DPAD_RIGHT == input):
            self.device.raise_brightness()

    def show_menu(self) :
        selected = Selection(None, None, 0)

        while(selected is not None):
            option_list = []
            option_list.append(
                GridOrListEntry(
                        primary_text="Power Off",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.shutdown
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
                        primary_text="Brightness",
                        value_text="<    " + str(self.device.brightness) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.brightness_adjust
                    )
            )
            option_list = DescriptiveListView(self.display,self.controller,self.device,self.theme, 
                                              "Settings", option_list, self.theme.get_list_small_selected_bg(),
                                              selected.get_index())
            selected = option_list.get_selection([ControllerInput.A, ControllerInput.DPAD_LEFT, ControllerInput.DPAD_RIGHT])

            if(selected is not None):
                selected.get_selection().get_value()(selected.get_input())
