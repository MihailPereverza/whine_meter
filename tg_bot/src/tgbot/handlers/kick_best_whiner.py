import contextlib

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from tgbot.repositories.backend import get_best_whiner

kick_best_whiner_router = Router()


@kick_best_whiner_router.message(Command(commands=['kick_best_whiner']))
async def kick_best_whiner(message: Message):
    assert message.bot is not None

    best_whiner = await get_best_whiner(chat_id=message.chat.id)
    if not best_whiner:
        return

    escaped_user_name = best_whiner.username.replace('_', '\_').replace('.', '\.').replace('-', '\-')
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile('tgbot/data/stop_whine.jpg'),
        caption=f'@{escaped_user_name}',
    )

    await message.chat.ban(user_id=best_whiner.id)
    with contextlib.suppress(Exception):
        await message.chat.unban(user_id=best_whiner.id)
