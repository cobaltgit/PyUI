class Theme():
    
    def __init__(self, path):
        self.path = path
    
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
    
    @property
    def text_color(self):
        # Get from json file
        return  (255, 255, 255) 
      
    @property
    def text_color_selected(self):
        # Get from json file
        return  (255, 255, 0)    
    
