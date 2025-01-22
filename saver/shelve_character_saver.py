import shelve
from typing import List, Dict, Any

from loguru import logger

from saver.base_character_saver import BaseCharacterSaver


class ShelveCharacterSaver(BaseCharacterSaver):
    def save_characters(self, characters: List[Dict[str, Any]], filename: str = 'characters.shelve') -> None:
        uniqe_characters = self.remove_duplicates(characters)
        try:
            with shelve.open(filename) as shelf:
                for character in uniqe_characters:
                    shelf[character['name']] = character
                logger.info(f"Successfully saved {len(uniqe_characters)} characters to {filename}")
        except Exception as e:
            logger.error(f"Error saving to shelve: {e}")


