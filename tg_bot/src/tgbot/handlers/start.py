from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello, I'm a bot\\!")
