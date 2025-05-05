
from controller.controller import Controller
from devices.device import Device
from devices.wifi.wifi_scanner import WiFiScanner
from display.display import Display
from themes.theme import Theme


class WifiMenu:
    def __init__(self, display : Display, controller: Controller, device: Device, theme: Theme):
        self.display : Display = display
        self.controller : Controller = controller
        self.device : Device= device
        self.theme : Theme= theme
        self.wifi_scanner = WiFiScanner()

    def scan_for_networks(self):
        networks = self.wifi_scanner.scan_networks()

        for net in networks:
            print(f"SSID: {net.ssid}, Signal: {net.signal_level} dBm, Frequency: {net.frequency} MHz, BSSID: {net.bssid}, Flags: {net.flags}")