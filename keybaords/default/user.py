from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def dynamic_reply_keyboard_builder(
        _,
        keyboards: list[dict[str, str]],
        extra_keyboards: list,
        adjust: int = 2,
        back_keyboard: bool = True,
        locale: str = 'en',

):
    builder = ReplyKeyboardBuilder()

    buttons = []
    for keyboard in keyboards:
        buttons.append(
            KeyboardButton(text=keyboard.get(locale))
        )

    builder.row(*buttons)
    builder.adjust(adjust)
    if extra_keyboards:
        builder.row(*extra_keyboards)
    if back_keyboard:
        builder.row(KeyboardButton(text=_("⬅️ Back")))

    return builder.as_markup(resize_keyboard=True)


async def share_contact(_):
    return ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text=_("☎️ Share phone number"), request_contact=True)
        ]], resize_keyboard=True
    )


async def share_location(_):
    return ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text=_("📍 Share my location"), request_location=True)
        ]], resize_keyboard=True
    )


async def user_main_menu(_):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🎓 Courses")),
                KeyboardButton(text=_("🎉 Events")),
            ],
            [
                KeyboardButton(text=_("☎️ Contacts")),
                KeyboardButton(text=_("⚙️ Settings")),
            ]
        ], resize_keyboard=True
    )
