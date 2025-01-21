import asyncio
from collections import defaultdict
from functools import lru_cache
import aiohttp
import requests

from character_fetcher.base_character_fetcher import BaseCharacterFetcher

BASEURL = 'https://swapi.dev/api/people/'

class StarWarsCharacterFetcher(BaseCharacterFetcher):
    def __init__(self):
        super().__init__(BASEURL, origin="Star Wars")
        self.results_per_page = 10
        self.species_cache = defaultdict(str)

    async def fetch_page(self, session, page):
        url = f"{self.base_url}?page={page}"
        return await self._make_request(session, url)

    async def fetch_characters_stream(self):
        async with aiohttp.ClientSession() as session:
            first_page = await self.fetch_page(session, 1)
            if not first_page:
                return
            number_of_characters = first_page.get('count')
            total_pages = (number_of_characters // self.results_per_page) + 1


            tasks = [self.fetch_page(session, page) for page in range(1, total_pages + 1)]

            for completed_task in asyncio.as_completed(tasks):
                page_data = await completed_task
                if page_data and 'results' in page_data:
                    for raw_character in page_data.get('results'):
                        yield self.normalize_character(raw_character)

    async def fetch_all_characters(self):
        return [character async for character in self.fetch_characters_stream()]

    def fetch_extra_info(self, url):
        return requests.get(url).json().get('name')

    def normalize_character(self, raw_character):
        species = 'Human'
        species_url = raw_character.get('species')

        if species_url:
            species_url = species_url[0]
            if self.species_cache[species_url]:
                species = self.species_cache[species_url]
            else:
                species = self.fetch_extra_info(species_url)
                self.species_cache[species_url] = species

        return {
            'name': raw_character.get('name'),
            'origin': self.origin,
            'species': species,
            'additional_attribute': raw_character.get('birth_year')
        }

if __name__ == '__main__':
    fetcher = StarWarsCharacterFetcher()
    characters = asyncio.run(fetcher.fetch_all_characters())
    print(characters)