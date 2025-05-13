

from controller.controller import Controller
from controller.controller_inputs import ControllerInput
from devices.device import Device
from display.display import Display
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.view_creator import ViewCreator
from views.view_type import ViewType


class InGameMenuPopup:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.view_creator = ViewCreator(display,controller,device,theme)

    def exit_game(self, input):
        return False

    def run_popup_menu_selection(self):
        popup_options = []
        popup_options.append(GridOrListEntry(
            primary_text="Exit Game",
            image_path=self.theme.settings,
            image_path_selected=self.theme.settings_selected,
            description="",
            icon=self.theme.settings,
            value=self.exit_game
        ))

        popup_view = self.view_creator.create_view(
            view_type=ViewType.TEXT_LIST_VIEW,
            options=popup_options,
            top_bar_text="Main Menu Sub Options",
            selected_index=0,
            cols=self.theme.popup_menu_cols,
            rows=self.theme.popup_menu_rows)
        
        while (popup_selection := popup_view.get_selection()):
            if(popup_selection.get_input() is not None):
                break
        
        if(ControllerInput.A == popup_selection.get_input()): 
            return popup_selection.get_selection().get_value()(popup_selection.get_input())