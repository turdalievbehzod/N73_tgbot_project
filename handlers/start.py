from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from filters.is_admin import IsAdmin
from keybaords.default.admin import admin_main_menu
from keybaords.default.user import share_contact, share_location, user_main_menu
from keybaords.inline.user import languages
from states.user import RegisterState
from utils.queries.users import get_user, add_user, update_user

router = Router()


@router.message(Command('start'), IsAdmin())
async def admin_start_handler(message: types.Message, state: FSMContext, _):
    text = _(f"Hello admin ") + message.from_user.full_name
    await message.answer(text=text, reply_markup=await admin_main_menu(_))
    await state.clear()


@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext, _):
    user = await get_user(chat_id=message.from_user.id)
    if user is None:
        text = _("🌏 Please select the language that you want")
        await message.answer(text=text, reply_markup=languages)
        await state.set_state(RegisterState.language)
    else:
        text = _(f"Hello welcome back, ") + message.from_user.full_name
        await message.answer(text=text, reply_markup=await user_main_menu(_))


@router.callback_query(RegisterState.language)
async def get_language_handler(call: types.CallbackQuery, state: FSMContext, _):
    await state.update_data(language=call.data, chat_id=call.from_user.id,
                            username=call.from_user.username)
    data = await state.get_data()
    await add_user(data=data)

    text = _("Please enter your full name", locale=call.data)
    await call.message.answer(text=text)
    await state.set_state(RegisterState.full_name)


@router.message(RegisterState.full_name)
async def get_full_name_handler(message: types.Message, state: FSMContext, _):
    await state.update_data(full_name=message.text)

    text = _("👇 Please enter your phone number by button on the below")
    await message.answer(text=text, reply_markup=await share_contact(_))
    await state.set_state(RegisterState.phone_number)


@router.message(RegisterState.phone_number, F.contact)
async def get_phone_number_handler(message: types.Message, state: FSMContext, _):
    await state.update_data(phone_number=message.contact.phone_number)

    text = _("👇 Please enter your location by button on the below")
    await message.answer(text=text, reply_markup=await share_location(_))
    await state.set_state(RegisterState.location)


@router.message(RegisterState.location, F.location)
async def get_location_handler(message: types.Message, state: FSMContext, _):
    await state.update_data(
        longitude=message.location.longitude,
        latitude=message.location.latitude
    )
    data = await state.get_data()
    new_user = await update_user(data=data, message=message)
    if new_user:
        text = _("✅ Successfully registered")
        await message.answer(text=text, reply_markup=await user_main_menu(_))
    else:
        text = _("❌ Something went wrong, please try again later")
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.clear()
