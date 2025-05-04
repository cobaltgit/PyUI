import json

from games.utils.favorite import Favorite

class MiyooFavoritesParser:

    def __init__(self):
        pass

    def parse_favorites(self):
        # List to hold the parsed JSON objects
        entries = []
        file_path = '/mnt/sdcard/Roms/favourite.json'

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # Ignore empty lines
                    try:
                        data = json.loads(line)
                        entry = Favorite(
                            label=data['label'],
                            launch=data['launch'],
                            rom_path=data['rompath'],
                            type=data['type']
                        )
                        entries.append(entry)
                        print(f"Adding favorite : {entry.rom_path}")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line: {line}\n{e}")

        return entries
