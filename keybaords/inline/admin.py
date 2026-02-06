from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class CourseCallback(CallbackData, prefix="course"):
    course_id: int
    is_active: int
    action: str


async def course_detail_keyboard(course_id: int, is_active: bool, _):
    if is_active:
        button_text = _("✅ Active")
    else:
        button_text = _("🛑 Inactive")

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=_("❌ Delete"), callback_data=CourseCallback(
                course_id=course_id, is_active=is_active, action="delete"
            ).pack()),
            InlineKeyboardButton(text=button_text, callback_data=CourseCallback(
                course_id=course_id, is_active=is_active, action="update_status"
            ).pack()),
        ]]
    )

    return markup
