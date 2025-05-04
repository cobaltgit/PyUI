from abc import ABC, abstractmethod

from games.utils.favorite import Favorite

class Device(ABC):
 
    @property
    @abstractmethod
    def screen_width(self):
        pass

    @property
    @abstractmethod
    def screen_height(self):
        pass
    
    @property
    @abstractmethod
    def font_size_small(self):
        pass    

    @property
    @abstractmethod
    def font_size_medium(self):
        pass   

    @property
    @abstractmethod
    def font_size_large(self):
        pass

    @property
    @abstractmethod
    def max_rows_for_list(self):
        pass

    @property
    @abstractmethod
    def max_icons_for_large_grid_view(self):
        pass

    @property
    @abstractmethod
    def large_grid_x_offset(self):
        pass

    @property
    @abstractmethod
    def large_grid_y_offset(self):
        pass
    
    @property
    @abstractmethod
    def large_grid_spacing_multiplier(self):
        pass

    @abstractmethod
    def get_app_finder(self):
        pass
    
    @abstractmethod
    def get_wifi_status(self):
        pass

    @abstractmethod
    def get_charge_status(self):
        pass

    @abstractmethod
    def get_battery_percent(self):
        pass

    @abstractmethod
    def run_game(self, path):
        pass

    @abstractmethod
    def run_app(self, args):
        pass

    @abstractmethod
    def map_input(self, sdl_input):
        pass

    @abstractmethod
    def parse_favorites(self) -> list[Favorite]:
        pass