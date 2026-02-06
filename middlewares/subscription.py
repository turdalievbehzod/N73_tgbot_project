from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from core.config import CHANNEL_ID
from keybaords.inline.user import channel_keyboard


class CheckSubscription(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        bot = data['bot']
        user_id = event.from_user.id
        _ = data.get('_')

        memberships = ['creator', 'administrator', 'member', 'restricted']
        member = await bot.get_chat_member(
            chat_id=CHANNEL_ID, user_id=user_id
        )
        if member.status in memberships:
            return await handler(event, data)
        else:
            text = _("Please join this channel")
            # For Message events
            if isinstance(event, Message):
                await event.answer(text=text, reply_markup=channel_keyboard)
            elif isinstance(event, CallbackQuery):
                await event.message.answer(text=text, reply_markup=channel_keyboard)
            return
