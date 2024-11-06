from io import BytesIO

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
# , get_user_graph, get_daily_graph)

from tgbot.repositories.backend import get_best_whiner

whine_sampler_router = Router()


@whine_sampler_router.message(Command(commands=['week_whine', 'нытье_недели']))
async def week_whine(message: Message):
    best_whiner = await get_best_whiner(chat_id=message.chat.id)
    if best_whiner:
        return await message.answer(f'Лучший нытик недели: {best_whiner.username}')
    return await message.answer('На этой неделе никто не ныл :\\)')


@whine_sampler_router.message(Command(commands=['daily_graph', 'график_дней']))
async def daily_graph(message: Message):
    graph = await get_daily_graph(chat_id=message.chat.id)
    return await message.reply_photo(BufferedInputFile(graph, filename="graph.png"))


@whine_sampler_router.message(Command(commands=['user_graph', 'график_пользователей']))
async def user_graph(message: Message):
    graph = await get_user_graph(chat_id=message.chat.id)
    return await message.reply_photo(BufferedInputFile(graph, filename="graph.png"))
