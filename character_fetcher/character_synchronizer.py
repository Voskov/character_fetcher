import asyncio
from typing import List, Optional

from icecream import ic
from loguru import logger
from character_fetcher.base_character_fetcher import BaseCharacterFetcher
from character_fetcher.pokemon_character_fetcher import PokemonCharacterFetcher
from character_fetcher.rick_and_morty_character_fetcher import RickAndMortyCharacterFetcher
from character_fetcher.star_wars_character_fetcher import StarWarsCharacterFetcher
from saver.saver_factory import get_saver, SaverType


class CharacterSynchronizer:
    def __init__(self, character_fetchers: List[BaseCharacterFetcher] = None,
                 db_type: SaverType = SaverType.JSON):
        self.fetchers = character_fetchers or [
            PokemonCharacterFetcher(),
            RickAndMortyCharacterFetcher(),
            StarWarsCharacterFetcher()
        ]
        self.db_type = db_type

    async def sync_characters_stream(self) -> List[dict]:
        logger.info("Starting character synchronization")
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
        logger.info("Character synchronization completed")

    @staticmethod
    async def _process_universe(fetcher) -> Optional[List[dict]]:
        logger.info(f"Fetching characters from {fetcher.config.name}")
        try:
            return await fetcher.fetch_all_characters()
        except Exception as e:
            logger.error(f"Error fetching characters from {fetcher.config.name}: {e}")
            return None


    async def synchronize(self) -> List[dict]:
        logger.info("Synchronizing characters")
        all_characters = []
        async for character in self.sync_characters_stream():
            if character:
                all_characters.append(character)
        logger.info(f"Total characters fetched: {len(all_characters)}")
        return sorted(all_characters, key=lambda c: c['name'])

    def save_characters(self, characters_list: List[dict]) -> None:
        logger.info(f"Saving characters to {self.db_type.name}")
        saver = get_saver(self.db_type)
        saver.save_characters(characters_list)
        logger.info("Characters saved successfully")


async def main():
    synchronizer = CharacterSynchronizer()
    all_characters = await synchronizer.synchronize()
    synchronizer.save_characters(all_characters)
    return all_characters

if __name__ == "__main__":
    characters = asyncio.run(main())
    ic(f"Total characters: {len(characters)}")
