
from controller.controller_inputs import ControllerInput
from menus.settings.theme.theme_settings_menu_common import ThemeSettingsMenuCommon
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry


class ThemeSettingsMainMenu(ThemeSettingsMenuCommon):
    def __init__(self):
        super().__init__()

    def change_main_menu_column_count(self, input):
        column_count = Theme.get_main_menu_column_count()

        if (ControllerInput.DPAD_LEFT == input):
            column_count = max(1, column_count-1)
        elif (ControllerInput.DPAD_RIGHT == input):
            column_count += 1  # Should we limit?

        Theme.set_main_menu_column_count(column_count)

    def build_column_enabled_entry(self, primary_text, get_value_func, set_value_func) -> GridOrListEntry:

        return GridOrListEntry(
            primary_text=primary_text,
            value_text="<    " + str(get_value_func()) + "    >",
            image_path=None,
            image_path_selected=None,
            description=None,
            icon=None,
            value=lambda input: self.change_enabled_disabled(
                input, get_value_func, set_value_func)
        )

    def build_options_list(self) -> list[GridOrListEntry]:
        option_list = []
        option_list.append(
            GridOrListEntry(
                primary_text="Main Menu",
                value_text="<    " + Theme.get_view_type_for_main_menu().name + "    >",
                image_path=None,
                image_path_selected=None,
                description=None,
                icon=None,
                value=lambda input: self.change_view_type(
                    input, Theme.get_view_type_for_main_menu, Theme.set_view_type_for_main_menu)
            )
        )
        option_list.append(
            GridOrListEntry(
                primary_text="Main Menu Columns",
                value_text="<    " +
                str(Theme.get_main_menu_column_count()) + "    >",
                image_path=None,
                image_path_selected=None,
                description=None,
                icon=None,
                value=self.change_main_menu_column_count
            )
        )
        option_list.append(
            self.build_column_enabled_entry(
                primary_text="Show Recents",
                get_value_func=Theme.get_recents_enabled,
                set_value_func=Theme.set_recents_enabled
            )
        )
        option_list.append(
            self.build_column_enabled_entry(
                primary_text="Show Favorites",
                get_value_func=Theme.get_favorites_enabled,
                set_value_func=Theme.set_favorites_enabled
            )
        )
        option_list.append(
            self.build_column_enabled_entry(
                primary_text="Show Apps",
                get_value_func=Theme.get_apps_enabled,
                set_value_func=Theme.set_apps_enabled
            )
        )
        option_list.append(
            self.build_column_enabled_entry(
                primary_text="Show Settings",
                get_value_func=Theme.get_settings_enabled,
                set_value_func=Theme.set_settings_enabled
            )
        )
        return option_list
