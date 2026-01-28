from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    language = State()
    full_name = State()
    phone_number = State()
    location = State()