# импорт необходимых модулей для работы
from aiogram.utils import executor
from create_bot import dp

async def on_startup(_):
    print('Bot online. OK!')

# импорт хендлеров
from client import client

client.register_handlers_client(dp)
# start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)