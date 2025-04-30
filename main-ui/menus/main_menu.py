
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from menus.games.system_select_menu import SystemSelectMenu
from themes.theme import Theme
from views.image_text_pair import ImageTextPair
from views.large_grid_view import LargeGridView


class MainMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.system_select_menu = SystemSelectMenu(display,controller,device,theme)

    def run_main_menu_selection(self):
        image_text_list = [
            ImageTextPair(self.theme.favorite, self.theme.favorite_selected, "Favorite"),
            ImageTextPair(self.theme.game,self.theme.game_selected, "Game"),
            ImageTextPair(self.theme.app,self.theme.app_selected, "App"),
            ImageTextPair(self.theme.settings,self.theme.settings_selected, "Setting")
        ]

        options_list = LargeGridView(self.display,self.controller,self.device,self.theme, image_text_list)
        selected = "new"
        while((selected := options_list.get_selection()) is not None):        
            print(f"{selected.get_text()} was selected")
            if(selected.get_text() == "Game"):
                self.system_select_menu.run_system_selection()
