from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

languages = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="🇺🇸 English", callback_data="en"),
        InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
    ]]
)