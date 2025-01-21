from abc import ABC, abstractmethod
from loguru import logger
import aiohttp


class BaseCharacterFetcher(ABC):
    def __init__(self, base_url: str, origin: str) -> None:
        self.base_url = base_url
        self.origin = origin

    @abstractmethod
    async def fetch_all_characters(self):
        pass

    @abstractmethod
    async def normalize_character(self, raw_character):
        pass

    async def _make_request(self, session: aiohttp.ClientSession, url: str):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return None

