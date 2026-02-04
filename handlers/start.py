from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keybaords.default.user import share_contact, share_location, user_main_menu, courses_menu, nt_info_menu
from keybaords.inline.user import languages
from states.user import CoursesState, RegisterState, ContactsState
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
        await message.answer(text=f"Hello, {message.from_user.full_name}", reply_markup=user_main_menu)


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
    
@router.message(F.text == "🎓 Courses")
async def courses_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="📖 Choose a course:",
        reply_markup=courses_menu
    )
    await state.set_state(CoursesState.courses)


@router.message(CoursesState.courses)
async def course_info_handler(message: types.Message, state: FSMContext):
    courses_info = {
        "🐍 Python": "Python course:\nDuration: 3 months\nLevel: Beginner → Advanced",
        "🌐 Web Development": "Web Dev course:\nHTML, CSS, JS, Django",
        "🤖 AI & ML": "AI & ML:\nNeural networks, Python, Math",
        "📱 Mobile Development": "Mobile Dev:\nFlutter, Android basics"
    }

    if message.text == "⬅ Back":
        await state.clear()
        await message.answer("Main menu", reply_markup=user_main_menu)
        return

    info = courses_info.get(message.text)
    if not info:
        await message.answer("❌ Please choose a course using buttons")
        return

    await message.answer(info)

@router.message(F.text == "☎️ Contacts")
async def courses_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="📖 Choose your learning center:",
        reply_markup=nt_info_menu
    )
    await state.set_state(ContactsState.lc_info)
    
@router.message(ContactsState.lc_info)
async def lc_info_handler(message: types.Message, state: FSMContext):
    nt_info = {
        "NAJOT TA'LIM O'QUV MARKAZI":   "100095, Toshkent, Olmazor tumani, Kichik Halqa Yo'li ko'chasi, 72A",
        "XADRA FILIALI":                "100011, Toshkent, Shayxontohur tumani, Xadra dahasi, Sebzor ko'chasi, 1",
        "CHILONZOR FILIALI":	        "100097, Toshkent, Chilonzor tumani, Qatortol ko'chasi, 1B",
        "SAMARQAND FILIALI":	        "Samarqand viloyati, Samarqand, Rudaki ko'chasi, 225",
        "XORAZM FILIALI":	            "Xorazm viloyati, Urganch, Al-Xorazmiy ko'chasi, 68B",
        "FARG'ONA FILIALI":	            "150117, Farg'ona viloyati, Farg'ona, Kuvasoy ko'chasi"
    }
    if message.text == "⬅ Back":
        await state.clear()
        await message.answer("Main menu", reply_markup=user_main_menu)
        return
    info = nt_info.get(message.text)
    if not info:
        await message.answer("❌ Please choose your option using buttons")
        return
    
    await message.answer(info)        