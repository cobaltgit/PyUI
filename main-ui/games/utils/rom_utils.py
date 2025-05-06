import os

class RomUtils:
    def __init__(self, roms_path):
        self.roms_path = roms_path

    def get_roms_path(self):
        return self.roms_path
    
    def get_roms(self, system):
        directory = os.path.join(self.roms_path, system)
        valid_files = sorted(
            entry.path for entry in os.scandir(directory)
            if entry.is_file(follow_symlinks=False)
            and not entry.name.startswith('.')
            and not entry.name.endswith(('.xml', '.txt', '.db'))
        )
        return valid_files