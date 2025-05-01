
class ImageTextPair:
    def __init__(self, text: str, image_path: str,image_path_selected: str = None, value = None):
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

    def get_image_path(self):
        return self.image_path
    
    def get_image_path_selected(self):
        return self.image_path_selected

    def get_text(self):
        return self.text
    
    def get_value(self):
        return self.value
