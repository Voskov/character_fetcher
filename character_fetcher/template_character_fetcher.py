import asyncio

import aiohttp

from character_fetcher.base_character_fetcher import BaseCharacterFetcher

BASEURL = 'https://swapi.dev/api/people/'

class TemplateCharacterFetcher(BaseCharacterFetcher):
    def __init__(self):
        super().__init__(BASEURL)

    async def fetch_page(self, session, page):
        url = f"{self.base_url}?page={page}"
        return await self._make_request(session, url)

    async def fetch_characters_stream(self):
        async with aiohttp.ClientSession() as session:
            first_page = await self.fetch_page(session, 1)
            if not first_page:
                return

            total_pages = 1 # REPLACE
            tasks = [self.fetch_page(session, page) for page in range(1, total_pages + 1)]

            for completed_task in asyncio.as_completed(tasks):
                page_data = await completed_task
                if page_data and 'results' in page_data:
                    for raw_character in page_data.get('results'):
                        yield self.normalize_character(raw_character)

    async def fetch_all_characters(self):
        return [character async for character in self.fetch_characters_stream()]

    def normalize_character(self, raw_character):
        return {
            'name': raw_character.get('name'),
        }

if __name__ == '__main__':
    fetcher = TemplateCharacterFetcher()
    characters = asyncio.run(fetcher.fetch_all_characters())
    print(characters)