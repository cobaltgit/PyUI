
class ImageTextPair:
    def __init__(self, image_path: str,image_path_selected: str, text: str):
        self.image_path = image_path
        self.image_path_selected = image_path_selected
        self.text = text

    def get_image_path(self):
        return self.image_path
    
    def get_image_path_selected(self):
        return self.image_path_selected

    def get_text(self):
        return self.text
