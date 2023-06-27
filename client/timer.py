from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
import pymorphy2

from client.generate_words import KEY
from client.status import Status
from keyboard.keyboard import function_button


async def time_game_text(bot: Bot, state: FSMContext, msg_id, chat_id, apscheduler):
    try:
        user_data = await state.get_data()
        print('timer:', user_data)
        print(msg_id)
        print(chat_id)
        morph = pymorphy2.MorphAnalyzer()
        sec = morph.parse('секунда')[0]
        time = user_data["time"] - 1

        if time == -1:
            await bot.send_message(chat_id=chat_id, text='Вы проиграли. Начните заново',
                                   reply_markup=function_button(['старт']))
            apscheduler.remove_job('id' + str(user_data["step"]))
            await state.set_state(Status.main)
            await bot.edit_message_text(text=f"Время вышло!", chat_id=int(chat_id)
                                        , message_id=int(msg_id))


            # await state.finish()

            # return

        text = f"Осталось: {time} {sec.make_agree_with_number(time).word}"
        print(text)
        await state.update_data(time=time)
        await bot.edit_message_text(text, chat_id, msg_id)

    except Exception as e:
        print(e)
        # await bot.send_message('Что-то пошло не так')
