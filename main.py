import asyncio
import logging
import sys
from os import getenv

import dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import devices_router
from middlewares import APIInjection

dotenv.load_dotenv()
TOKEN = getenv("BOT_TOKEN")
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(devices_router)
dp.message.outer_middleware(APIInjection())
dp.callback_query.outer_middleware(APIInjection())

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
