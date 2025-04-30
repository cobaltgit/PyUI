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
    def font_size(self):
        pass

    @property
    @abstractmethod
    def max_rows_for_list(self):
        pass