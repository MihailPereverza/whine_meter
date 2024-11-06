from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.repositories.postgres.messages import pg_get_best_whiner

week_whine_router = Router()


@week_whine_router.message(Command(commands=['week_whine', 'нытье_недели']))
async def week_whine(message: Message):
    best_whiner_id = await pg_get_best_whiner(chat_id=message.chat.id)
    return await message.answer(f'Лучший нытик недели: {best_whiner_id}')