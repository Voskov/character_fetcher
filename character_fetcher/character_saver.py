from enum import Enum, auto
import json
import shelve
import sqlite3
from typing import Dict, Any
from tinydb import TinyDB
from loguru import logger

class SaverType(Enum):
    JSON = auto()
    SHELVE = auto()
    TINYDB = auto()
    SQLITE = auto()


class CharacterSaver:
    def __init__(self, saver_type: SaverType):
        self.saver_type = saver_type

    def save_characters(self, characters: list) -> None:
        match self.saver_type:
            case SaverType.JSON:
                self.save_json(characters)
            case SaverType.SHELVE:
                self.save_shelve(characters)
            case SaverType.TINYDB:
                self.save_tinydb(characters)
            case SaverType.SQLITE:
                self.save_sqlite(characters)

    @staticmethod
    def remove_duplicates(characters: list) -> list:
        """
        Remove duplicate characters based on the character's name.
        """
        unique_characters = []
        seen_names = set()
        for character in characters:
            name = character['name']
            if name not in seen_names:
                unique_characters.append(character)
                seen_names.add(name)
        return unique_characters

    @staticmethod
    def save_json(characters: list, filename: str = 'characters.json') -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(characters, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved {len(characters)} characters to {filename}")
        except IOError as e:
            logger.error(f"Error saving to file: {e}")

    @staticmethod
    def save_shelve(characters: list, filename: str = 'characters.shelve') -> None:
        logger.info(f"Saving characters to shelve: {filename}")
        try:
            with shelve.open(filename) as shelf:
                for character in characters:
                    shelf[character['name']] = character
            logger.info(f"Successfully saved {len(characters)} characters to {filename}")
        except Exception as e:
            logger.error(f"Error saving to shelve: {e}")


    @staticmethod
    def save_tinydb(characters: list, filename: str = 'characters.tiny') -> None:
        try:
            db = TinyDB(filename)
            table = db.table('characters')
            table.truncate()  # Clear existing data

            # Convert characters dict to list if it's not already
            if isinstance(characters, dict):
                characters_list = list(characters.values())
            else:
                characters_list = characters

            table.insert_multiple(characters_list)
            logger.info(f"Successfully saved {len(characters_list)} characters to TinyDB: {filename}")
            db.close()
        except Exception as e:
            logger.error(f"Error saving to TinyDB: {e}")

    @staticmethod
    def save_sqlite(characters: list, filename: str = 'characters.db') -> None:
        characters = CharacterSaver.remove_duplicates(characters)
        try:
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()

            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS characters (
                    name TEXT PRIMARY KEY,
                    data TEXT
                )
            ''')

            # Clear existing data
            cursor.execute('DELETE FROM characters')

            # Insert characters
            for character in characters:
                cursor.execute(
                    'INSERT INTO characters (name, data) VALUES (?, ?)',
                    (character['name'], json.dumps(character))
                )

            conn.commit()
            logger.info(f"Successfully saved {len(characters)} characters to SQLite: {filename}")
            conn.close()
        except Exception as e:
            logger.error(f"Error saving to SQLite: {e}")

    @staticmethod
    def load_characters(saver_type: SaverType, filename: str) -> Dict[str, Any]:
        """
        Load characters from the specified storage type.
        Returns a dictionary of characters.
        """
        try:
            match saver_type:
                case SaverType.JSON:
                    with open(filename, 'r', encoding='utf-8') as f:
                        return json.load(f)

                case SaverType.SHELVE:
                    characters = {}
                    with shelve.open(filename) as shelf:
                        for key in shelf.keys():
                            characters[key] = shelf[key]
                    return characters

                case SaverType.TINYDB:
                    db = TinyDB(filename)
                    table = db.table('characters')
                    characters = {char['name']: char for char in table.all()}
                    db.close()
                    return characters

                case SaverType.SQLITE:
                    conn = sqlite3.connect(filename)
                    cursor = conn.cursor()
                    cursor.execute('SELECT name, data FROM characters')
                    characters = {name: json.loads(data) for name, data in cursor.fetchall()}
                    conn.close()
                    return characters

        except Exception as e:
            logger.error(f"Error loading characters: {e}")
            return {}