from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from tgbot.settings.base import settings

pg_engine = create_async_engine(settings.database_url, echo=settings.debug_mode)
pg_session = sessionmaker(bind=pg_engine, class_=AsyncSession, expire_on_commit=False, autoflush=True) # type: ignore