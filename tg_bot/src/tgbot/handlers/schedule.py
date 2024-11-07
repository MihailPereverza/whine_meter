from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CommandObject
from datetime import datetime
from whine_samplers import daily_graph


scheduler_router = Router()

@scheduler_router.message(Command("set_date_time"))
async def cmd_set_date_time(message: Message, command: CommandObject):
    data = command.args
    if len(data) == 1:
        await message.answer("Неверный формат")
        return
    date = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(daily_graph, 'cron', hour=date.hour, minute=date.minute, second=date.second, start_date=date, args=[message])
    scheduler.start()
    await message.answer("Время установлено")