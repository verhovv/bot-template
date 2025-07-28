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

from core.handlers import router
from core.logger import setup_loger

from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis


async def main():
    setup_loger()

    bot = Bot(token=config.BOT_TOKEN)

    redis = Redis(host=config.REDIS_HOST if not config.DEBUG else 'localhost', port=config.REDIS_PORT, db=1)
    storage = RedisStorage(redis)

    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
