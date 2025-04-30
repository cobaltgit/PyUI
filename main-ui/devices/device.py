from abc import ABC, abstractmethod

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