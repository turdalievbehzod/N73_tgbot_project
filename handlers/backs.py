from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from keybaords.default.admin import admin_main_menu
from states.admin import CourseDetailState

router = Router()


@router.message(F.text == "⬅️ Back", CourseDetailState.search)
async def get_course_handler(message: types.Message, state: FSMContext, _):
    text = _("Welcome back to main menu")
    await message.answer(text=text, reply_markup=await admin_main_menu(_))
    await state.clear()
