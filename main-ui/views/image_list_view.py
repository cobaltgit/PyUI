from typing import List
from controller.controller_inputs import ControllerInput
from display.display import Display
from display.font_purpose import FontPurpose
import sdl2
from devices.device import Device
from controller.controller import Controller
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.list_view import ListView

class ImageListView(ListView):

    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, top_bar_text,
                 options: List[GridOrListEntry], img_offset_x : int, img_offset_y : int):
        super().__init__(controller)
        self.display = display
        self.device = device
        self.theme = theme
        self.top_bar_text = top_bar_text
        self.options = options

        self.selected = 0
        self.line_height = display.get_line_height(FontPurpose.LIST) + 10  # add 10px padding between lines
        self.current_top = 0
        self.max_rows = device.max_rows_for_list
        self.current_bottom = min(self.max_rows,len(options))
        self.img_offset_x = img_offset_x
        self.img_offset_y = img_offset_y
     

    def _render_text(self, visible_options):
        for visible_index, (imageTextPair) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
            color = self.theme.text_color_selected(FontPurpose.LIST) if actual_index == self.selected else self.theme.text_color(FontPurpose.LIST)
            self.display.render_text(imageTextPair.get_text(), 50, self.display.get_top_bar_height() + 5 + visible_index * self.line_height, color, FontPurpose.LIST)

    def _render_image(self, visible_options):
        for visible_index, (imageTextPair) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
            imagePath = imageTextPair.get_image_path_selected() if actual_index == self.selected else imageTextPair.get_image_path()
            if(actual_index == self.selected and imagePath is not None):
                self.display.render_image_centered(imagePath, 
                                     self.img_offset_x, 
                                     self.img_offset_y)

    def _render(self):
        visible_options = self.options[self.current_top:self.current_bottom]

        #ensure image is rendered last so it is on top of the text
        self._render_text(visible_options)
        self._render_image(visible_options)

        self.display.present()
