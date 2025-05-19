
from controller.controller_inputs import ControllerInput
from menus.settings.theme.theme_settings_menu_common import ThemeSettingsMenuCommon
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry


class ThemeSettingsSystemSelectMenu(ThemeSettingsMenuCommon):
    def __init__(self):
        super().__init__()

    def build_options_list(self) -> list[GridOrListEntry]:
        option_list = []
        option_list.append(
            self.build_view_type_entry(
                primary_text="System Sel Menu",
                get_value_func=Theme.get_view_type_for_system_select_menu,
                set_value_func=Theme.set_view_type_for_system_select_menu
            )
        )
        return option_list
