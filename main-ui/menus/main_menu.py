
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from menus.app.app_menu import AppMenu
from menus.games.system_select_menu import SystemSelectMenu
from themes.theme import Theme
from views.grid_view import GridView
from views.image_text_pair import ImageTextPair


class MainMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.system_select_menu = SystemSelectMenu(display,controller,device,theme)
        self.app_menu = AppMenu(display,controller,device,theme)

    def run_main_menu_selection(self):
        image_text_list = [
            ImageTextPair( "Favorite", self.theme.favorite, self.theme.favorite_selected),
            ImageTextPair("Game", self.theme.game,self.theme.game_selected),
            ImageTextPair("App",self.theme.app,self.theme.app_selected),
            ImageTextPair("Setting", self.theme.settings,self.theme.settings_selected)
        ]

        options_list = GridView(self.display,self.controller,self.device,self.theme, "SPRUCE", image_text_list, 4, 1)
        selected = "new"
        while((selected := options_list.get_selection()) is not None):        
            if(selected.get_text() == "Game"):
                self.system_select_menu.run_system_selection()
            elif(selected.get_text() == "App"):
                self.app_menu.run_app_selection()
