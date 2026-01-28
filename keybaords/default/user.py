from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

share_contact = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="☎️ Share phone number", request_contact=True)
    ]], resize_keyboard=True
)

share_location = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="📍 Share my location", request_location=True)
    ]], resize_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎓 Courses"),
            KeyboardButton(text="🎉 Events"),
        ],
        [
            KeyboardButton(text="☎️ Contacts"),
            KeyboardButton(text="⚙️ Settings"),
        ]
    ], resize_keyboard=True
)