from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keybaords.default.user import share_contact, share_location, user_main_menu
from keybaords.inline.user import languages
from states.user import RegisterState
from utils.queries.users import get_user, add_user

router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.from_user.id)
    if user is None:
        text = "🌏 Please select the language that you want"
        await message.answer(text=text, reply_markup=languages)
        await state.set_state(RegisterState.language)
    else:
        await message.answer(text=f"Salom, {message.from_user.full_name}")


@router.callback_query(RegisterState.language)
async def get_language_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(language=call.data)

    text = "Please enter your full name"
    await call.message.answer(text=text)
    await state.set_state(RegisterState.full_name)


@router.message(RegisterState.full_name)
async def get_full_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    text = "👇 Please enter your phone number by button on the below"
    await message.answer(text=text, reply_markup=share_contact)
    await state.set_state(RegisterState.phone_number)


@router.message(RegisterState.phone_number, F.contact)
async def get_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)

    text = "👇 Please enter your location by button on the below"
    await message.answer(text=text, reply_markup=share_location)
    await state.set_state(RegisterState.location)


@router.message(RegisterState.location, F.location)
async def get_location_handler(message: types.Message, state: FSMContext):
    await state.update_data(
        longitude=message.location.longitude,
        latitude=message.location.latitude
    )
    data = await state.get_data()
    new_user = await add_user(data=data, message=message)
    if new_user:
        text = "✅ Successfully registered"
        await message.answer(text=text, reply_markup=user_main_menu)
    else:
        text = "❌ Something went wrong, please try again later"
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.clear()