import datetime
import re
from math import inf

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from client.generate_words import generate_words
from client.status import Status
from client.timer import time_game_text
from create_bot import dp, bot, apscheduler
from info.info_text import text_info
from keyboard.keyboard import function_button


async def command_start(message: types.Message, state: FSMContext):
    try:
        await Status.main.set()
        text = text_info["start"]
        await message.reply_sticker(text["sticker"])
        await message.reply(text["text"], reply_markup=function_button(['старт']))
        await message.delete()
    except Exception as e:
        await message.reply('‼ Общение происходит в лс‼')


@dp.message_handler(lambda msg: msg.text == 'старт', state=Status.main)
async def start_timer(message: types.Message):
    try:
        text = text_info["timer"]
        await message.reply(text["text"], reply_markup=function_button(text["button"]))
        await Status.game.set()
        # await message.delete()
    except Exception as e:
        await message.reply('Что-то пошло не так')


@dp.message_handler(lambda msg: msg.text in text_info["timer"]["button"], state=Status.game)
async def time_game(message: types.Message, state: FSMContext):
    try:
        apscheduler.remove_all_jobs()

        msg = message.text
        if msg == '10 сек.':
            timer = 10
        elif msg == '15 сек.':
            timer = 15
        elif msg == '20 сек.':
            timer = 20
        else:
            timer = -1

        await state.update_data(timer=timer)
        await state.update_data(time=timer)
        await state.update_data(step=0)

        if timer != -1:
            msg = await message.answer(f"Осталось: {timer} секунд", reply_markup=function_button(['стоп']))
            print('msg', msg)
            apscheduler.add_job(time_game_text, trigger='interval', seconds=1,
                                kwargs={'bot': bot, 'state': state, 'msg_id': msg["message_id"],
                                        'chat_id': message.chat.id,
                                        "apscheduler": apscheduler},
                                id='id0')


            apscheduler.start()
        else:
            await message.answer(f"Ваш ход",  reply_markup=function_button(['стоп']))
        await state.update_data(flag=True)
    except Exception as e:
        # await message.reply(f'Что-то пошло не так ----- {e}')
        pass


@dp.message_handler(lambda msg: msg.text not in text_info["timer"]["button"], state=Status.game)
async def game(message: types.Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        # apscheduler: AsyncIOScheduler = user_data["apscheduler"]

        timer = user_data["timer"]
        await state.update_data(time=timer)
        # apscheduler.pause()
        print(user_data)

        msg = message.text.lower()
        msg = re.sub('\W+', '', msg)

        if user_data["flag"]:
            await state.update_data(step=user_data["step"] + 1)
            if timer != -1:
                apscheduler.remove_job('id' + str(user_data["step"]))
                _msg = await message.answer(f"Осталось: {timer} секунд")
                print('_msg', _msg)
                # apscheduler.remove_all_jobs()

                apscheduler.add_job(time_game_text, trigger='interval', seconds=1,
                                    kwargs={'bot': bot, 'state': state, 'msg_id': _msg["message_id"],
                                            'chat_id': message.chat.id,
                                            "apscheduler": apscheduler},
                                    id='id' + str(user_data["step"] + 1))
        if msg != 'стоп':
            if user_data['step'] == 0 and user_data['time'] != 0:
                letter = msg[-1]
                word = generate_words(letter)
                await state.update_data(word=word[-1])
                await message.answer(word)
                # apscheduler.start()
                await state.update_data(flag=True)
            elif user_data['step'] > 0 and user_data['time'] != 0:
                if user_data["word"] == msg[0]:
                    letter = msg[-1]
                    word = generate_words(letter)
                    await state.update_data(word=word[-1])
                    await message.answer(word)
                    # apscheduler.start()
                    await state.update_data(flag=True)
                else:
                    await state.update_data(flag=False)
                    await message.answer("Вы ввели неверное слово")
        else:
            await message.answer("Спасибо за игру", reply_markup=function_button(['старт']))
            # await state.finish()
            await state.set_state(Status.main)
            # apscheduler.pause()


    except Exception as e:
        print(e, 'game')
        # await message.reply(f'Что-то пошло не так - game, \n{e}')
        pass


def register_handlers_client(dp):
    dp.register_message_handler(command_start, commands=['start', 'help'], state='*')
    dp.register_message_handler(start_timer, lambda msg: msg.text == 'старт', state='*')
