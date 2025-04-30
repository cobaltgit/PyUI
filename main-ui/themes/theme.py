from abc import ABC, abstractmethod

class Theme(ABC):
    @property
    @abstractmethod
    def background(self):
        pass

    @property
    @abstractmethod
    def favorite(self):
        pass

    @property
    @abstractmethod
    def favorite_selected(self):
        pass

    @property
    @abstractmethod
    def game(self):
        pass

    @property
    @abstractmethod
    def game_selected(self):
        pass

    @property
    @abstractmethod
    def app(self):
        pass

    @property
    @abstractmethod
    def app_selected(self):
        pass

    @property
    @abstractmethod
    def settings(self):
        pass

    @property
    @abstractmethod
    def settings_selected(self):
        pass