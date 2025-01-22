from typing import List, Dict, Any

from tinydb import TinyDB
from loguru import logger

from saver.base_character_saver import BaseCharacterSaver


class TinyDBCharacterSaver(BaseCharacterSaver):
    def save_characters(self, characters: List[Dict[str, Any]], filename: str = 'characters.tinydb') -> None:
        try:
            db = TinyDB(filename)
            table = db.table('characters')
            db.insert_multiple(characters)
            db.close()
            logger.info(f"Successfully saved {len(characters)} characters to {filename}")
        except Exception as e:
            logger.error(f"Error saving to TinyDB: {e}")