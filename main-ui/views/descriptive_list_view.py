from typing import List
from controller.controller_inputs import ControllerInput
from display.display import Display
from display.font_purpose import FontPurpose
import sdl2
from devices.device import Device
from controller.controller import Controller
from themes.theme import Theme
from views.descriptive_list_view_entry import DescriptiveListViewEntry
from views.image_text_pair import ImageTextPair
from views.list_view import ListView

class DescriptiveListView(ListView):

    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, top_bar_text,
                 options: List[DescriptiveListViewEntry]):
        super().__init__(controller)
        self.display = display
        self.device = device
        self.theme = theme
        self.top_bar_text = top_bar_text
        self.options = options

        self.selected = 0
        self.current_top = 0
        self.max_rows = device.max_rows_for_descriptive_list
        self.current_bottom = min(self.max_rows,len(options))
        self.spacing = 10
     

    def _render(self):
        visible_options = self.options[self.current_top:self.current_bottom]

        row_offset_x = self.theme.get_descriptive_list_icon_offset_x()
        row_offset_y = self.display.get_top_bar_height() + 5
        
        for visible_index, (imageTextPair) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
            iconPath = imageTextPair.get_icon()

            if actual_index == self.selected:
                selected_bg = self.theme.get_descriptive_list_selected_bg()
                self.bg_w, self.bg_h = self.display.render_image(
                    selected_bg, 
                    0, 
                    row_offset_y)
                
            icon_w, icon_h = self.display.render_image(iconPath, 
                                row_offset_x, 
                                row_offset_y + self.theme.get_descriptive_list_icon_offset_y())

            color = self.theme.text_color_selected(FontPurpose.DESCRIPTIVE_LIST_TITLE) if actual_index == self.selected else self.theme.text_color(FontPurpose.DESCRIPTIVE_LIST_TITLE)
            title_w, title_h = self.display.render_text(
                imageTextPair.get_title(), 
                row_offset_x + icon_w + self.theme.get_descriptive_list_text_from_icon_offset(), 
                row_offset_y + self.theme.get_descriptive_list_text_offset_y(), 
                color, 
                FontPurpose.DESCRIPTIVE_LIST_TITLE)

            color = self.theme.text_color_selected(FontPurpose.DESCRIPTIVE_LIST_DESCRIPTION) if actual_index == self.selected else self.theme.text_color(FontPurpose.DESCRIPTIVE_LIST_DESCRIPTION)
            
            text_w, text_h = self.display.render_text(
                imageTextPair.get_title(), 
                row_offset_x + icon_w + self.theme.get_descriptive_list_text_from_icon_offset(), 
                row_offset_y + + self.theme.get_descriptive_list_text_offset_y() + title_h, 
                color, 
                FontPurpose.DESCRIPTIVE_LIST_DESCRIPTION)

            row_offset_y += self.bg_h + self.spacing

        self.display.present()
