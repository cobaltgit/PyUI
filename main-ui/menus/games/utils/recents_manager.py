
from dataclasses import dataclass
import json
from typing import List, Optional
from devices.device_common import DeviceCommon
from games.utils.game_system_utils import GameSystemUtils
from menus.games.utils.rom_info import RomInfo
from menus.games.utils.roms_list_manager import RomsListEntry, RomsListManager
from utils.logger import PyUiLogger

class RecentsManager:
    _recentsManager = Optional[RomsListManager]

    @classmethod
    def initialize(cls, recents_path: str):
        cls._recentsManager = RomsListManager(recents_path)

    @classmethod
    def add_game(cls, rom_info: RomInfo):
        cls._recentsManager.add_game(rom_info)
        games = cls._recentsManager.get_games()
        if len(games) > 20:
            for game in games[20:]:
                cls._recentsManager.remove_game(game)
                
    @classmethod
    def get_recents(cls) -> List[RomInfo]:
        return cls._recentsManager.get_games()
