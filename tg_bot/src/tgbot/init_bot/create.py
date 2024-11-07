import logging
from collections.abc import Awaitable, Callable
from typing import Any, Dict

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import TelegramObject

from tgbot.handlers.add_to_chat import add_to_chat_router
from tgbot.handlers.all_message_in_group import all_messages_in_group_router
from tgbot.handlers.start import start_router
from tgbot.handlers.whine_samplers import whine_sampler_router
from tgbot.handlers.schedule import scheduler_router
from tgbot.repositories.backend import check_backend
from tgbot.settings.base import settings

logger = logging.getLogger(__name__)


class EventInterceptorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict,
    ) -> Awaitable[Any]:
        # Process the event here
        print(f"Intercepted event: {event}")
        return await handler(event, data)


class BotService:
    def __init__(self):
        self._bot = Bot(token=settings.tg_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
        self._storage = MemoryStorage()
        self.db = Dispatcher(storage=self._storage)
        self._register_handlers()

    def _register_handlers(self):
        self.db.include_router(start_router)
        self.db.include_router(add_to_chat_router)
        self.db.include_router(whine_sampler_router)
        self.db.include_router(scheduler_router)
        self.db.include_router(all_messages_in_group_router)

    @property
    def aiogram_bot(self) -> Bot:
        return self._bot

    async def check_backend(self):
        success, err = await check_backend()
        if not success:
            print(f"Failed to connect to backend: {err}")
            exit(1)

    async def start_polling(self):
        await self.check_backend()
        self.db.update.middleware(EventInterceptorMiddleware())
        await self.db.start_polling(self._bot)
