from themes.theme import Theme

class SpruceTheme(Theme):
    
    @property
    def background(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/background.png"

    @property
    def favorite(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/ic-favorite-n.png"

    @property
    def favorite_selected(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/ic-favorite-f.png"    

    @property
    def game(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/ic-game-n.png"    

    @property
    def game_selected(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/ic-game-f.png"    

    @property
    def app(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/ic-app-n.png"    
    @property
    def app_selected(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/ic-app-f.png"    

    @property
    def settings(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/ic-setting-n.png"    

    @property
    def settings_selected(self):
        return "/mnt/sdcard/Themes/SPRUCE/skin/ic-settingHow -f.png"    
