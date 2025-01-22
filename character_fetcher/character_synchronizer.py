import asyncio
import json
from typing import List
from loguru import logger
from character_fetcher.base_character_fetcher import BaseCharacterFetcher
from character_fetcher.pokemon_character_fetcher import PokemonCharacterFetcher
from character_fetcher.rick_and_morty_character_fetcher import RickAndMortyCharacterFetcher
from character_fetcher.star_wars_character_fetcher import StarWarsCharacterFetcher


class CharacterSynchronizer:
    def __init__(self, character_fetchers: List[BaseCharacterFetcher] = None):
        self.fetchers = character_fetchers or [
            PokemonCharacterFetcher(),
            RickAndMortyCharacterFetcher(),
            StarWarsCharacterFetcher()
        ]

    async def sync_characters_stream(self):
        fetch_tasks = [
            asyncio.create_task(self._process_universe(fetcher))
            for fetcher in self.fetchers
        ]

        for completed_task in asyncio.as_completed(fetch_tasks):
            try:
                characters = await completed_task
                if characters:
                    for character in characters:
                        yield character
            except Exception as e:
                logger.error(f"Error processing task: {e}")

    async def _process_universe(self, fetcher):
        try:
            return await fetcher.fetch_all_characters()
        except Exception as e:
            logger.error(f"Error fetching characters from {fetcher.__class__.__name__}: {e}")
            return None

    async def synchronize(self):
        all_characters = []
        async for character in self.sync_characters_stream():
            if character:
                all_characters.append(character)
        return sorted(all_characters, key=lambda c: c['name'])

    def save_to_file(self, characters: List[dict], filename: str = "characters.json"):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(characters, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved {len(characters)} characters to {filename}")
        except IOError as e:
            logger.error(f"Error saving to file: {e}")


async def main():
    synchronizer = CharacterSynchronizer()
    all_characters = await synchronizer.synchronize()
    synchronizer.save_to_file(all_characters)
    return all_characters

if __name__ == "__main__":
    characters = asyncio.run(main())
    print(f"Total characters: {len(characters)}")
