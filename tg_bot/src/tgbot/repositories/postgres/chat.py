from sqlalchemy.dialects.postgresql import insert

from tgbot.entities.chat import Chat
from tgbot.mappers.chat import chat_serializer
from tgbot.repositories.postgres import pg_session
from tgbot.repositories.postgres.pg_tables.chats import chats_table


async def pg_save_chat(*, chat: Chat) -> None:
    values = chat_serializer.dump(chat)

    async with pg_session() as session, session.begin():
            await session.execute(
                insert(chats_table)
                .values(values)
                .on_conflict_do_update(
                    index_elements=[chats_table.c.id],
                    set_=values
                )
            )
