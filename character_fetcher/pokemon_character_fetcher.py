import asyncio

import aiohttp
import requests

from character_fetcher.base_character_fetcher import BaseCharacterFetcher

BASEURL = 'https://pokeapi.co/api/v2'

class PokemonCharacterFetcher(BaseCharacterFetcher):
    def __init__(self):
        super().__init__(BASEURL, "Pokémon")
        self.page_size = 100

    def get_number_of_characters(self):
        response = requests.get(f"{self.base_url}/pokemon?limit=1&offset=0")
        return response.json().get('count')

    async def fetch_page(self, session: aiohttp.ClientSession, offset: int):
        url = f"{self.base_url}/pokemon?limit={self.page_size}&offset={offset}"
        return await self._make_request(session, url)

    async def fetch_pokemon_urls(self):
        number_of_characters = self.get_number_of_characters()
        session = aiohttp.ClientSession()
        tasks = [self.fetch_page(session, offset) for offset in range(0, number_of_characters, self.page_size)]

        pokemons = []

        for completed_task in asyncio.as_completed(tasks):
            page_data = await completed_task
            if page_data and 'results' in page_data:
                pokemons.extend(page_data.get('results'))
        return [p['url'] for p in pokemons]

    async def fetch_pokemon_details(self, session, url):
        return await self._make_request(session, url)

    async def fetch_characters_stream(self):
        async with aiohttp.ClientSession() as session:
            pokemon_urls = await self.fetch_pokemon_urls()
            tasks = [self.fetch_pokemon_details(session, url) for url in pokemon_urls]

            for completed_task in asyncio.as_completed(tasks):
                raw_character = await completed_task
                if not raw_character:
                    continue
                yield self.normalize_character(raw_character)

    def normalize_character(self, raw_character):
        types = '/'.join([t['type']['name'].title() for t in raw_character.get('types')])
        return {
            'name': raw_character.get('name').title(),
            'origin': self.origin,
            'species': types,
            'additional_attribute': raw_character.get('base_experience')
        }

    async def fetch_all_characters(self):
        return [character async for character in self.fetch_characters_stream()]

if __name__ == '__main__':
    fetcher = PokemonCharacterFetcher()
    characters = asyncio.run(fetcher.fetch_all_characters())
    print(characters)
