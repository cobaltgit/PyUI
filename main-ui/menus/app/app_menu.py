

from controller.controller import Controller
from devices.device import Device
from display.display import Display
from themes.theme import Theme
from views.descriptive_list_view import DescriptiveListView
from views.descriptive_list_view_entry import DescriptiveListViewEntry


class AppMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display= display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.appFinder = device.get_app_finder()



    def run_app_selection(self) :
        selected = "new"
        app_list = []
        for app in self.appFinder.get_apps():
            if(app.get_label() is not None):
                app_list.append(
                    DescriptiveListViewEntry(
                        app.get_label(),
                        app.get_description(),
                        app.get_icon(),
                        app.get_launch()
                    )
                )

        options_list = DescriptiveListView(self.display,self.controller,self.device,self.theme, "Apps", app_list)
        while((selected := options_list.get_selection()) is not None):
            self.device.run_app(selected.get_value())
            self.controller.clear_input_queue()
            self.display.reinitialize()
