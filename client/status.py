from aiogram.dispatcher.filters.state import StatesGroup, State


class Status(StatesGroup):
    # We set two main States
    main = State()  # main menu
    game = State()