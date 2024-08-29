import asyncio
import logging

from aiogram.methods import DeleteWebhook
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from app import handler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_routers(handler.router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
