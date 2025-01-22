from abc import ABC, abstractmethod
import asyncio
import aiohttp
from loguru import logger

from multiverse.universe_config import UniverseConfig


class BaseCharacterFetcher(ABC):
    def __init__(self, config: UniverseConfig) -> None:
        self.config = config
        self.base_url = config.base_url
        self.origin = config.name

    @abstractmethod
    async def fetch_all_characters(self):
        pass

    @abstractmethod
    async def normalize_character(self, raw_character):
        return self.config.character_mapper(raw_character)

    async def _make_request(self, session: aiohttp.ClientSession, url: str):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Client error fetching data from {url}: {e}")
        except asyncio.TimeoutError:
            logger.error(f"Timeout while fetching data from {url}")
        except Exception as e:
            logger.error(f"Unexpected error fetching data from {url}: {e}")
        return None
