from dataclasses import dataclass

@dataclass
class UniverseConfig:
    name: str
    base_url: str

class UniverseConfigs:
    POKEMON = UniverseConfig(
        name='Pokémon',
        base_url='https://pokeapi.co/api/v2/pokemon/',
    )
    RICK_AND_MORTY = UniverseConfig(
        name='Rick and Morty',
        base_url='https://rickandmortyapi.com/api/character/',
    )
    STAR_WARS = UniverseConfig(
        name='Star Wars',
        base_url='https://swapi.dev/api/people/',
    )
