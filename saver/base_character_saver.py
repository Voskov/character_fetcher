from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseCharacterSaver(ABC):
    @abstractmethod
    def save_characters(self, characters: List[Dict[str, Any]], filename: str) -> None:
        pass

    @staticmethod
    def remove_duplicates(characters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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

