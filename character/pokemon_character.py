from dataclasses import dataclass

from character.base_charachter import BaseCharacter
from multiverse.universe_config import UniverseConfigs


@dataclass
class PokemonCharacter(BaseCharacter):
    def __init__(self, name: str, origin: str, species: str, base_experience: str) -> 'PokemonCharacter':
        super().__init__(name, origin, species, additional_attribute = base_experience)

    @classmethod
    def from_raw_character(cls, raw_character: dict) -> 'BaseCharacter':
        types = '/'.join([t['type']['name'].title() for t in raw_character.get('types')])
        return cls(
            name = raw_character.get('name').title(),
            origin = UniverseConfigs.POKEMON.name,
            species = types,
            base_experience = raw_character.get('base_experience')
        )
