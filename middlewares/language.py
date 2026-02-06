from pathlib import Path
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from babel.support import Translations


class I18nMiddleware(BaseMiddleware):
    def __init__(self, locales_dir: Path, domain: str = "messages"):
        self.locales_dir = locales_dir
        self.domain = domain
        self.translations = {}
        self._load_translations()
        super().__init__()

    def _load_translations(self):
        """Load all translations"""
        for locale_dir in self.locales_dir.iterdir():
            if locale_dir.is_dir():
                locale = locale_dir.name
                try:
                    self.translations[locale] = Translations.load(
                        dirname=str(self.locales_dir),
                        locales=[locale],
                        domain=self.domain
                    )
                except Exception as e:
                    print(f"Failed to load {locale}: {e}")

    def gettext(self, message: str, locale: str = None):
        """
        Get translation for a specific locale
        If locale is None, returns the message as-is
        """
        if locale and locale in self.translations:
            return self.translations[locale].gettext(message)
        return message

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user: User = data.get("event_from_user")

        if user:
            # Get user language from database
            from utils.queries.users import get_user
            user_data = await get_user(user.id)

            if user_data and "language" in user_data:
                user_locale = user_data["language"]
            else:
                user_locale = "uz"  # default

            # Get translation function for this locale
            trans = self.translations.get(user_locale)
            if trans:
                data["i18n"] = trans

                # Create a flexible _ function that accepts locale parameter
                def _(text: str, locale: str = None):
                    if locale:
                        return self.gettext(text, locale)
                    return trans.gettext(text)

                data["_"] = _
            else:
                # Fallback
                data["_"] = lambda text, locale=None: self.gettext(text, locale) if locale else text

            data["locale"] = user_locale
            data["i18n_middleware"] = self  # Give access to middleware

        return await handler(event, data)
