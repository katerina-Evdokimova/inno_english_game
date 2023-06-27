from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def function_button(my_list):
    replay_button = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in my_list:
        replay_button.add(KeyboardButton(i))
    return replay_button


# replay_button = InlineKeyboardMarkup()
# replay_button.add(InlineKeyboardButton('Как ты?', callback_data='str1'))
def function_inline_button(my_list):
    replay_button = InlineKeyboardMarkup()
    for i in my_list:
        replay_button.add(InlineKeyboardButton(i, callback_data=i))
    return replay_button