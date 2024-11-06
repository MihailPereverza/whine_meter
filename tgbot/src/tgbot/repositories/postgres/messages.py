
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from tgbot.entities.message import Message
from tgbot.mappers.message import message_serializer
from tgbot.repositories.postgres import pg_session
from tgbot.repositories.postgres.pg_tables.messages import messages_table


async def pg_save_message(*, message: Message) -> None:
    """Сохранить сообщение в базу данных"""

    values = message_serializer.dump(message)

    async with pg_session() as session, session.begin():
        await session.execute(
            messages_table.insert()
            .values(values)
        )

    return None


async def pg_get_best_whiner(chat_id: int) -> int:
    """Получить ID пользователя, который больше всех пожаловался за неделю"""

    # max(count(whine_value > 0.5))
    query = (
        select(
            messages_table.c.user_id,
            count(messages_table.c.whine_value > 0.5).label('whine_count'),
        )
        .where(
            messages_table.c.chat_id == chat_id,
        )
        .group_by(
            messages_table.c.user_id,
        )
        .order_by(
            text('whine_count DESC'),
        )
    )
    session: AsyncSession
    async with pg_session() as session, session.begin():
        res = await session.execute(query)
        res_data = res.fetchone()
        assert res_data is not None
        return res_data.user_id
