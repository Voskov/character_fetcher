import json
from typing import List, Dict, Any
import sqlite3
from loguru import logger

from saver.base_character_saver import BaseCharacterSaver


class SqliteCharacterSaver(BaseCharacterSaver):
    def save_characters(self, characters: List[Dict[str, Any]], filename: str = 'characters.sqlite') -> None:
        unique_characters = self.remove_duplicates(characters)
        try:
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS characters (
                    name TEXT PRIMARY KEY,
                    data TEXT
                )
            ''')

            for character in characters:
                cursor.execute(
                    'INSERT INTO characters (name, data) VALUES (?, ?)',
                    (character['name'], json.dumps(character))
                )
            conn.commit()
            logger.info(f"Successfully saved {len(unique_characters)} characters to SQLite: {filename}")
        except Exception as e:
            logger.error(f"Error saving to SQLite: {e}")