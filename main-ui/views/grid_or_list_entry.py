

class GridOrListEntry:
    def __init__(self, text, image_path = None,image_path_selected = None, 
                 description = None, icon = None, value = None):
        self.text = text
        self.image_path = image_path

        if(image_path_selected is None):
            self.image_path_selected = image_path
        else:
            self.image_path_selected = image_path_selected

        if(value is None): 
            self.value = text
        else:
            self.value = value

        self.description = description
        self.icon = icon

    def get_image_path(self):
        return self.image_path
    
    def get_image_path_selected(self):
        return self.image_path_selected
    
    def get_text(self):
        return self.text
    
    def get_value(self):
        return self.value
    
    def get_description(self):
        return self.description

    def get_icon(self):
        return self.icon
    
    def get_value(self):
        return self.value
