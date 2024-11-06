from datetime import UTC, datetime
from random import random

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Filter
from aiogram.types import Message as TGMessage

from tgbot.entities.message import Message
from tgbot.entities.user import User
from tgbot.repositories.postgres.messages import pg_save_message
from tgbot.repositories.postgres.users import pg_upsert_user

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
    await pg_upsert_user(
        user=User(
            id=tg_message.from_user.id,
            username=tg_message.from_user.username,
            first_name=tg_message.from_user.first_name,
            last_name=tg_message.from_user.last_name,
            language_code=tg_message.from_user.language_code,
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
            deleted_at=None,
            role='user',
        ),
    )

    now = datetime.now(tz=UTC)
    return await pg_save_message(
        message=Message(
            id=tg_message.message_id,
            chat_id=tg_message.chat.id,
            user_id=tg_message.from_user.id,
            text=tg_message.text,
            whine_value=random(),
            created_at=now,
            updated_at=now,
            deleted_at=None,
            old_versions=[],
        ),
    )
