
from dataclasses import dataclass
import json
from typing import List, Optional
from devices.device import Device
from games.utils.game_system_utils import GameSystemUtils
from menus.games.utils.rom_info import RomInfo
from menus.games.utils.roms_list_manager import RomsListEntry, RomsListManager
from utils.logger import PyUiLogger

class FavoritesManager:
    _favoritesManager = Optional[RomsListManager]

    @classmethod
    def initialize(cls, favorites_path: str):
        cls._favoritesManager = RomsListManager(favorites_path)

    @classmethod
    def add_favorite(cls, rom_info: RomInfo):
        cls._favoritesManager.add_favorite(rom_info)

    @classmethod
    def remove_favorite(cls, rom_info: RomInfo):
        cls._favoritesManager.remove_favorite(rom_info)

    @classmethod
    def is_favorite(cls, rom_info: RomInfo) -> bool:
        return cls._favoritesManager.is_favorite(rom_info)

    @classmethod
    def get_favorites(cls) -> List[RomInfo]:
        return cls._favoritesManager.get_favorites()
