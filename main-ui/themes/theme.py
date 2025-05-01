import json
import os

from display.font_purpose import FontPurpose

class Theme():
    
    def __init__(self, path):
        self.path = path
        self.load_from_file(os.path.join(path,"config.json"))

    
    def load_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Store top-level keys as attributes
        for key, value in data.items():
            setattr(self, key, value)

    @property
    def background(self):
        return self.path + "skin/background.png"

    @property
    def favorite(self):
        return self.path + "skin/ic-favorite-n.png"

    @property
    def favorite_selected(self):
        return self.path + "skin/ic-favorite-f.png"    

    @property
    def game(self):
        return self.path + "skin/ic-game-n.png"    

    @property
    def game_selected(self):
        return self.path + "skin/ic-game-f.png"    

    @property
    def app(self):
        return self.path + "skin/ic-app-n.png"    
    
    @property
    def app_selected(self):
        return self.path + "skin/ic-app-f.png"    

    @property
    def settings(self):
        return self.path + "skin/ic-setting-n.png"    

    @property
    def settings_selected(self):
        return self.path + "skin/ic-setting-f.png"    
    
    def system(self, system):
        return self.path + "icons/" + system.lower() +".png"
    
    def system_selected(self, system):
        return self.path + "icons/sel/" + system.lower() +".png"
    
    def get_font(self, font_purpose : FontPurpose):
        match font_purpose:
            case FontPurpose.GRID_ONE_ROW:
                return os.path.join(self.path,self.grid["font"]) 
            case FontPurpose.GRID_MULTI_ROW:
                return os.path.join(self.path,self.grid["font"]) 
            case FontPurpose.LIST:
                return os.path.join(self.path,self.grid["font"]) 
            case _:
                return os.path.join(self.path,self.list["font"]) 
    
    def get_font_size(self, font_purpose : FontPurpose):
        match font_purpose:
            case FontPurpose.GRID_ONE_ROW:
                return self.grid["grid1x4"]
            case FontPurpose.GRID_MULTI_ROW:
                return self.grid["grid3x4"]
            case FontPurpose.LIST:
                return self.list["size"]
            case _:
                return self.list["font"]


    @property
    def text_color(self):
        # Get from json file
        return  (255, 255, 255) 
      
    @property
    def text_color_selected(self):
        # Get from json file
        return  (215, 180, 95)    
    
