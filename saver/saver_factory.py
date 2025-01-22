from enum import Enum, auto

from saver.base_character_saver import BaseCharacterSaver


class SaverType(Enum):
    JSON = auto()
    SHELVE = auto()
    TINYDB = auto()
    SQLITE = auto()

def get_saver(saver_type: SaverType) -> BaseCharacterSaver:

    match saver_type:
        case SaverType.JSON:
            from saver.json_character_saver import JsonCharacterSaver
            return JsonCharacterSaver()
        case SaverType.SHELVE:
            from saver.shelve_character_saver import ShelveCharacterSaver
            return ShelveCharacterSaver()
        case SaverType.TINYDB:
            from saver.tinydb_character_saver import TinyDBCharacterSaver
            return TinyDBCharacterSaver()
        case SaverType.SQLITE:
            from saver.sqlite_character_saver import SqliteCharacterSaver
            return SqliteCharacterSaver()
        case _:
            raise ValueError(f"Invalid saver type: {saver_type}")