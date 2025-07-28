import logging
from pathlib import Path
import django
import sys
import os

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.core.settings")
django.setup()

from aiogram import Bot, Dispatcher
from config import config
import asyncio

from bot.core.handlers import router

from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis


async def main():
    bot = Bot(token=config.BOT_TOKEN)

    redis = Redis(host=config.REDIS_HOST if not config.DEBUG else 'redis', port=config.REDIS_PORT, db=1)
    storage = RedisStorage(redis)

    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    await dp.start_polling(bot)


if __name__ == '__main__':
    a = 0
    asyncio.run(main())
