from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.entities.user import User
from tgbot.mappers.user import user_serializer
from tgbot.repositories.postgres import pg_session
from tgbot.repositories.postgres.pg_tables.users import users_table


async def pg_upsert_user(user: User) -> None:
    values = user_serializer.dump(user)

    query = (
        insert(users_table)
        .values(user_serializer.dump(user))
        .on_conflict_do_update(
            index_elements=[users_table.c.id],
            set_=values,
        )
    )

    session: AsyncSession
    async with pg_session() as session, session.begin():
        await session.execute(query)

    return None
