from datetime import UTC, datetime

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Filter
from aiogram.types import Message as TGMessage

from tgbot.entities.message import Message
from tgbot.entities.user import User
from tgbot.handlers.add_to_chat import save_chat
from tgbot.repositories.backend import upsert_user, save_message

all_messages_in_group_router = Router()


class IsGroupChat(Filter):
    async def __call__(self, message: TGMessage) -> bool:
        return message.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}


@all_messages_in_group_router.message(IsGroupChat())
async def all_messages_in_group(tg_message: TGMessage):
    if not tg_message.text:
        return
    if not tg_message.from_user:
        return
    if not tg_message.from_user.username:
        return

    await save_chat(tg_message.chat)

    await upsert_user(
        user=User(
            id=tg_message.from_user.id,
            username=tg_message.from_user.username,
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
            role='user',
        ),
    )

    now = datetime.now(tz=UTC)
    return await save_message(
        message=Message(
            id=tg_message.message_id,
            chat_id=tg_message.chat.id,
            user_id=tg_message.from_user.id,
            text=tg_message.text,
            created_at=now,
            updated_at=now,
        ),
    )
