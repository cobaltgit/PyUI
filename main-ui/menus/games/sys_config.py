import json
import os

class SysConfig:
    def __init__(self, system_name):
        self.system_name = system_name
        config_path = f"/mnt/sdcard/Emu/{system_name}/config.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as f:
            self.config = json.load(f)

    def get_icon(self):
        return self.config.get("icon")
    
    def get_icon_selected(self):
        return self.config.get("iconsel")