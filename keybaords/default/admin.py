from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def admin_main_menu(_):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🎓 Courses")),
                KeyboardButton(text=_("🎉 Events")),
            ],
            [
                KeyboardButton(text=_("⬆️ Send message")),
                KeyboardButton(text=_("⚙️ Settings")),
            ]
        ], resize_keyboard=True
    )
