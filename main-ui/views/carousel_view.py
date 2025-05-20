from typing import List
from controller.controller_inputs import ControllerInput
from devices.device import Device
from display.font_purpose import FontPurpose
from display.display import Display
from display.render_mode import RenderMode
import sdl2
from controller.controller import Controller
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.selection import Selection
from views.view import View

class CarouselView(View):
    def __init__(self,top_bar_text, options: List[GridOrListEntry], cols : int, 
                  selected_index=0, show_grid_text=False, resized_width=None, resized_height=None, 
                  set_top_bar_text_to_selection=False, resize_type=None):
        super().__init__()
        self.resized_width = resized_width
        self.resized_height = resized_height
        self.resize_type = resize_type
        self.top_bar_text = top_bar_text
        self.set_top_bar_text_to_selection = set_top_bar_text_to_selection
        self.options : List[GridOrListEntry] = options 

        self.max_img_height = resized_height
        if(self.max_img_height is None):
            self.max_img_height = 0
            for option in options:           
                self.max_img_height = max(self.max_img_height, Display.get_image_dimensions(option.get_image_path())[1])

        self.selected = selected_index
        self.toggles = [False] * len(options)

        self.cols = 3
        self.current_left = len(options)-(cols-1)//2
        self.current_right = (cols-1)//2


        self.font_purpose = FontPurpose.GRID_ONE_ROW

        self.show_grid_text = show_grid_text
     
    def set_options(self, options):
        self.options = options

    def correct_selected_for_off_list(self):
        if(self.selected < 0):
            self.selected = len(self.options)-1

        if(self.current_left < 0):
            self.current_left = len(self.options)-1

        if(self.current_right < 0):
            self.current_right = len(self.options)-1

        if(self.selected == len(self.options)):
            self.selected = 0

        if(self.current_left == len(self.options)):
            self.current_left = 0

        if(self.current_right == len(self.options)):
            self.current_right = 0

    def get_visible_options(self):
        n = len(self.options)
        # Normalize into [0, n)
        left = self.current_left % n
        right = self.current_right % n

        visible = []
        visible_indexes = []

        i = left
        while True:
            visible.append(self.options[i])
            visible_indexes.append(i)
            # stop as soon as we've just appended the inclusive `right`
            if i == right:
                break
            i = (i + 1) % n  # wrap around

        print(f"visible = {visible_indexes}")
        return visible


    def get_width_percentages(self) -> List[float]:
        mid_size = 40.0
        scale_size = (100.0 - mid_size) //2
        n = self.cols
        # 1) If n is even, bump it to odd
        if n % 2 == 0:
            n += 1

        # half‑width
        k = n // 2

        # the total “raw weight” on one side is 2^0 + 2^1 + … + 2^(k−1) = 2^k − 1
        total_raw = 2**k - 1

        # 3) we want the left sum to be exactly 25, so scale factor:
        scale = scale_size / total_raw

        # 4) left side doubles: 2^0,2^1,…,2^(k−1)
        left = [(2**i) * scale for i in range(k)]

        # 2) middle is 50
        mid = [mid_size]

        # 5) right side halves from the middle: use the reverse‐doubling sequence
        #    2^(k−1),2^(k−2),…,2^0, scaled to sum to 25
        right = [(2**(k - 1 - i)) * scale for i in range(k)]

        return left + mid + right


    def _render(self):
        if(self.set_top_bar_text_to_selection) and len(self.options) > 0:
            Display.clear(self.options[self.selected].get_primary_text(), hide_top_bar_icons=True)
        else:
            Display.clear(self.top_bar_text)
        self.correct_selected_for_off_list()

        visible_options: List[GridOrListEntry] = self.get_visible_options()

        #TODO Get hard coded values for padding from theme
        x_pad = 10
        usable_width = Device.screen_width()
        image_width_percentages = self.get_width_percentages()
        widths = [int(round(percent/100 * usable_width)) for percent in image_width_percentages]
        # x_offset[0] = 0; for i>0, sum of widths[0] through widths[i-1]
        x_offsets = [0] + [sum(widths[:i]) for i in range(1, len(widths))]
        print(f"x_offsets = {x_offsets}")
        
        for visible_index, imageTextPair in enumerate(visible_options):
            
            actual_index = self.current_left + visible_index
            image_path = imageTextPair.get_image_path_selected() if actual_index == self.selected else imageTextPair.get_image_path()
            
            x_index = visible_index % self.cols
            x_offset = x_offsets[x_index]

            y_image_offset = Display.get_center_of_usable_screen_height()
            render_mode = RenderMode.MIDDLE_LEFT_ALIGNED
            
            Display.render_image(image_path, 
                                    x_offset, 
                                    y_image_offset,
                                    render_mode,
                                    target_width=widths[x_index],
                                    target_height=self.resized_height,
                                    resize_type=self.resize_type)
            color = Theme.text_color_selected(self.font_purpose) if actual_index == self.selected else Theme.text_color(self.font_purpose)

            real_y_text_offset = int(Device.screen_height() * 325/480)

            if(self.show_grid_text) :
                Display.render_text_centered(imageTextPair.get_primary_text(), 
                                        x_offset,
                                        real_y_text_offset, color,
                                        self.font_purpose)
        
        Display.present()

    def get_selected_option(self):
        if 0 <= self.selected < len(self.options):
            return self.options[self.selected]
        else:
            return None

    def get_selection(self, select_controller_inputs = [ControllerInput.A]):
        self._render()
        
        if(Controller.get_input()):
            if Controller.last_input() == ControllerInput.DPAD_LEFT:
                self.selected-=1
                self.current_left-=1
                self.current_right-=1
                self.correct_selected_for_off_list()
            elif Controller.last_input() == ControllerInput.DPAD_RIGHT:
                self.selected+=1
                self.current_left+=1
                self.current_right+=1
                self.correct_selected_for_off_list()
            elif Controller.last_input() in select_controller_inputs:
                return Selection(self.get_selected_option(),Controller.last_input(), self.selected)
            elif Controller.last_input() == ControllerInput.B:
                return Selection(self.get_selected_option(),Controller.last_input(), self.selected)
                
        return Selection(self.get_selected_option(),None, self.selected)
