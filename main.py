import asyncio
from loguru import logger

from character_fetcher.character_saver import SaverType
from character_fetcher.character_synchronizer import CharacterSynchronizer

SAVER_TYPE = SaverType.JSON

async def main():
    """
    This function is the entry point of the application. It creates an instance of the CharacterSynchronizer class,
    """
    logger.info("Starting character synchronization process")
    
    synchronizer = CharacterSynchronizer()
    
    logger.info("Fetching characters from all universes")
    all_characters = await synchronizer.synchronize()

    logger.info(f"Saving characters to {SAVER_TYPE.name}")

    synchronizer.save_characters(all_characters, SAVER_TYPE)

    logger.info("Character synchronization process completed")

if __name__ == '__main__':
    asyncio.run(main())
