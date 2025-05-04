
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from menus.app.app_menu import AppMenu
from menus.games.favorites_menu import FavoritesMenu
from menus.games.game_system_select_menu import GameSystemSelectMenu
from menus.games.recents_menu import RecentsMenu
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.grid_view import GridView


class MainMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.system_select_menu = GameSystemSelectMenu(display,controller,device,theme)
        self.app_menu = AppMenu(display,controller,device,theme)
        self.favorites_menu = FavoritesMenu(display,controller,device,theme)
        self.recents_menu = RecentsMenu(display,controller,device,theme)
        
    def run_main_menu_selection(self):
        #TODO make this user config driven
        first_entry = "Favorite"

        image_text_list = [
            GridOrListEntry(
                        text=first_entry,
                        image_path=self.theme.favorite,
                        image_path_selected=self.theme.favorite_selected,
                        description=first_entry,
                        icon=self.theme.favorite_selected,
                        value=first_entry
            ),                    
            GridOrListEntry(
                        text="Game",
                        image_path=self.theme.game,
                        image_path_selected=self.theme.game_selected,
                        description="Your games",
                        icon=self.theme.game_selected,
                        value="Game"
            ),
            GridOrListEntry(
                        text="App",
                        image_path=self.theme.app,
                        image_path_selected=self.theme.app_selected,
                        description="Your Apps",
                        icon=self.theme.app_selected,
                        value="App"
            ),      
            GridOrListEntry(
                        text="Setting",
                        image_path=self.theme.settings,
                        image_path_selected=self.theme.settings_selected,
                        description="Your Apps",
                        icon=self.theme.settings_selected,
                        value="Setting"
            ),            
        ]

        options_list = GridView(self.display,self.controller,self.device,self.theme, "SPRUCE", image_text_list, 4, 1)
        selected = "new"
        while((selected := options_list.get_selection()) is not None):        
            if(selected.get_selection().get_text() == "Game"):
                self.system_select_menu.run_system_selection()
            elif(selected.get_selection().get_text() == "App"):
                self.app_menu.run_app_selection()
            elif(selected.get_selection().get_text() == "Favorite"):
                self.favorites_menu.run_rom_selection()
            elif(selected.get_selection().get_text() == "Recent"):
                self.recents_menu.run_rom_selection()
