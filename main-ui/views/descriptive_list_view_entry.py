
class DescriptiveListViewEntry:
    def __init__(self, title, description, icon, value):
        self.title = title
        self.description = description
        self.icon = icon
        self.value = value

    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description

    def get_icon(self):
        return self.icon
    
    def get_value(self):
        return self.value
    
