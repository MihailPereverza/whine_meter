import asyncio
import logging

from tgbot.init_bot.create import BotService
from tgbot.settings.base import settings

bot = BotService()


async def main():
    if settings.debug_mode:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    await bot.aiogram_bot.delete_webhook(drop_pending_updates=True)
    await bot.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
