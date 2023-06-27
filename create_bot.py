# импорт токена
from aiogram import Bot
from aiogram.dispatcher import Dispatcher, storage
from config import TOKEN
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.contrib.fsm_storage.memory import MemoryStorage  # хранение в оперативке

storage = MemoryStorage()
# инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
apscheduler = AsyncIOScheduler(timezone="Europe/Moscow")
# apscheduler.start()
# dp.middleware.register(SchedulerMiddleware(scheduler))
# dp.register_poll_handler(SchedulerMiddleware(scheduler))