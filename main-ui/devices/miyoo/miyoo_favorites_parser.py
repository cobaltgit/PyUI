import json

from games.utils.favorite import Favorite

class MiyooFavoritesParser:

    def __init__(self):
        pass

    def parse_favorites(self):
        file_path = '/mnt/sdcard/Roms/favourite.json'

        # List to hold the parsed JSON objects
        entries = []
        try:
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
                        except json.JSONDecodeError as e:
                            print(f"Error parsing line: {line}\n{e}")
        except (FileNotFoundError, IOError) as e:
            print(f"Could not read favorites file: {e}")
        return entries
