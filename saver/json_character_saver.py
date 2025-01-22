import json
from typing import List, Any, Dict

from loguru import logger

from saver.base_character_saver import BaseCharacterSaver


class JsonCharacterSaver(BaseCharacterSaver):
    def save_characters(self, characters: List[Dict[str, Any]], filename: str = 'characters.json') -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(characters, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved {len(characters)} characters to {filename}")
        except IOError as e:
            logger.error(f"Error saving to JSON file: {e}")
