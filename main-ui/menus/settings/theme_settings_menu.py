

from controller.controller_inputs import ControllerInput
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.selection import Selection
from views.view_creator import ViewCreator
from views.view_type import ViewType, get_next_view_type


class ThemeSettingsMenu():
    def __init__(self):
        pass

    def change_view_type(self, input, get_view_type_func, set_view_type_func):
        if input == ControllerInput.DPAD_LEFT:
            next_view_type = get_next_view_type(get_view_type_func(), -1)
        elif input == ControllerInput.DPAD_RIGHT:
            next_view_type = get_next_view_type(get_view_type_func(), +1)
        else:
            return  # No change for other inputs

        set_view_type_func(next_view_type)

    def change_main_menu_column_count(self, input):
        column_count = Theme.get_main_menu_column_count()

        if(ControllerInput.DPAD_LEFT == input):
            column_count = max(1, column_count-1)
        elif(ControllerInput.DPAD_RIGHT == input):
            column_count +=1 #Should we limit?

        Theme.set_main_menu_column_count(column_count)

    def build_options_list(self):
        option_list = []
        option_list.append(
                GridOrListEntry(
                        primary_text="Main Menu",
                        value_text="<    " + Theme.get_view_type_for_main_menu().name + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=lambda input: self.change_view_type(input, Theme.get_view_type_for_main_menu, Theme.set_view_type_for_main_menu)
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Game Sel Menu",
                        value_text="<    " + Theme.get_game_selection_view_type().name + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=lambda input: self.change_view_type(input, Theme.get_game_selection_view_type, Theme.set_game_selection_view_type)
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Main Menu Columns",
                        value_text="<    " + str(Theme.get_main_menu_column_count()) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.change_main_menu_column_count
                    )
            )
        return option_list

    def show_theme_options_menu(self):
        selected = Selection(None, None, 0)
        list_view = None
        self.theme_changed = False
        while(selected is not None):
            option_list = self.build_options_list()
            

            if(list_view is None or self.theme_changed):
                list_view = ViewCreator.create_view(
                    view_type=ViewType.ICON_AND_DESC,
                    top_bar_text="Settings", 
                    options=option_list,
                    selected_index=selected.get_index())
                self.theme_changed = False
            else:
                list_view.set_options(option_list)

            control_options = [ControllerInput.A, ControllerInput.DPAD_LEFT, ControllerInput.DPAD_RIGHT,
                                                  ControllerInput.L1, ControllerInput.R1]
            selected = list_view.get_selection(control_options)

            if(selected.get_input() in control_options):
                selected.get_selection().get_value()(selected.get_input())
            elif(ControllerInput.B == selected.get_input()):
                selected = None


