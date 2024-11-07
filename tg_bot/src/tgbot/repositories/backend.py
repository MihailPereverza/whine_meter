import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from httpx import AsyncClient
from serpyco_rs import Serializer

from tgbot.entities.chat import Chat
from tgbot.entities.message import Message
from tgbot.entities.user import User, PartialUser

user_serializer = Serializer(User)
message_serializer = Serializer(Message)
chat_serializer = Serializer(Chat)


@asynccontextmanager
async def backend_connection() -> AsyncIterator[AsyncClient]:
    backend_url = os.getenv("BACKEND_URL")
    assert backend_url is not None, "BACKEND_URL environment variable is not set"
    async with AsyncClient(base_url=backend_url) as sess:
        yield sess


async def check_backend():
    try:
        async with backend_connection() as connection:
            response = await connection.get("/healthcheck")
            response.raise_for_status()
    except Exception as e:
        return False, e
    else:
        return True, ""


async def save_chat(chat: Chat):
    values = chat_serializer.dump(chat)
    async with backend_connection() as connection:
        await connection.put("/chat", json=values)


async def upsert_user(user: User):
    values = user_serializer.dump(user)
    async with backend_connection() as connection:
        await connection.put("/user", json=values)


async def save_message(message: Message):
    values = message_serializer.dump(message)
    async with backend_connection() as connection:
        await connection.put("/message", json=values)


async def get_best_whiner(chat_id: int) -> PartialUser | None:
    async with backend_connection() as connection:
        data = (await connection.get("/whiner_otw", params={"chat_id": chat_id})).json()
        return PartialUser(**data) if data else None


async def get_daily_graph(chat_id: int) -> bytes:
    async with backend_connection() as connection:
        data = await connection.get("/graph/dates", params={"chat_id": chat_id})
        return data.content


async def get_user_graph(chat_id: int) -> bytes:
    async with backend_connection() as connection:
        data = await connection.get("/graph/users", params={"chat_id": chat_id})
        return data.content
