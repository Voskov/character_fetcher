from dataclasses import dataclass

from character.base_charachter import BaseCharacter
from multiverse.universe_config import UniverseConfigs


@dataclass
class RickAndMortyCharacter(BaseCharacter):
    def __init__(self, name: str, origin: str, species: str, status: str):
        super().__init__(name, origin, species, additional_attribute = status)


    @classmethod
    def from_raw_character(cls, raw_character: dict) -> 'RickAndMortyCharacter':
        return cls(
            name=raw_character.get('name'),
            origin=UniverseConfigs.RICK_AND_MORTY.name,
            species=raw_character.get('species'),
            status=raw_character.get('status')
        )
