from datetime import UTC, datetime

from aiogram import Router
from aiogram.types import Chat as TGChat
from aiogram.types import Message

from tgbot.entities.chat import Chat
from tgbot.repositories.backend import save_chat as backend_save_chat

add_to_chat_router = Router()


@add_to_chat_router.message(lambda message: message.chat.type == 'group' and message.group_chat_created)
async def create_chat(message: Message):
    await save_chat(tg_chat=message.chat)


@add_to_chat_router.message(lambda message: message.chat.type == 'group' and message.new_chat_members)
async def add_to_chat(message: Message):
    assert message.new_chat_members is not None
    assert message.bot is not None

    new_members_ids = [user.id for user in message.new_chat_members]

    bot_obj = await message.bot.get_me()
    if bot_obj.id not in new_members_ids:
        return

    return await save_chat(tg_chat=message.chat)


async def save_chat(tg_chat: TGChat) -> None:
    assert tg_chat.title

    now = datetime.now(tz=UTC)
    chat = Chat(id=tg_chat.id, title=tg_chat.title, type=tg_chat.type, created_at=now, updated_at=now)
    return await backend_save_chat(chat=chat)
