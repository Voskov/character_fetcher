from character.base_charachter import BaseCharacter
from multiverse.universe_config import UniverseConfigs


class StarWarsCharacter(BaseCharacter):
    def __init__(self, name: str, origin: str, species: str, birth_year: str):
        super().__init__(name, origin, species, additional_attribute = birth_year)

    @classmethod
    def from_raw_character(cls, raw_character: dict) -> 'StarWarsCharacter':
        return cls(
            name = raw_character.get('name'),
            origin = UniverseConfigs.STAR_WARS.name,
            species = raw_character.get('species'),
            birth_year = raw_character.get('birth_year')
        )
