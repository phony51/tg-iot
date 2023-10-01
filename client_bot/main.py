import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from config import configuration
from devices.handlers import devices_router

bot = Bot(token=configuration.bot.token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(devices_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
