from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    address = State()
    date = State()