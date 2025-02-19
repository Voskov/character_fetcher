import asyncio

import aiohttp
from icecream import ic

from character.rick_and_morty_character import RickAndMortyCharacter
from character_fetcher.base_character_fetcher import BaseCharacterFetcher
from multiverse.universe_config import UniverseConfigs


class RickAndMortyCharacterFetcher(BaseCharacterFetcher):
    def __init__(self) -> None:
        super().__init__(UniverseConfigs.RICK_AND_MORTY)

    async def fetch_page(self, session, page) -> dict:
        url = f"{self.base_url}?page={page}"
        return await self._make_request(session, url)

    async def fetch_characters_stream(self):
        async with aiohttp.ClientSession() as session:
            first_page = await self.fetch_page(session, 1)
            if not first_page:
                return

            total_pages = first_page.get('info').get('pages')

            tasks = [self.fetch_page(session, page) for page in range(1, total_pages + 1)]

            for completed_task in asyncio.as_completed(tasks):
                page_data = await completed_task
                if page_data and 'results' in page_data:
                    for raw_character in page_data.get('results'):
                        yield self.normalize_character(raw_character)

    async def fetch_all_characters(self) -> list:
        return [character async for character in self.fetch_characters_stream()]

    def normalize_character(self, raw_character) -> dict:
        rick_and_morty_character = RickAndMortyCharacter.from_raw_character(raw_character)
        return rick_and_morty_character.to_dict()

if __name__ == '__main__':
    fetcher = RickAndMortyCharacterFetcher()
    characters = asyncio.run(fetcher.fetch_all_characters())
    ic(characters)
