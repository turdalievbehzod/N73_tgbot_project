from pathlib import Path

from middlewares.language import I18nMiddleware
from middlewares.subscription import CheckSubscription

I18N_DOMAIN = "messages"
LOCALES_DIR = Path("locales")


def setup_middlewares(dp):
    """Setup i18n middleware"""
    # language middleware
    i18n = I18nMiddleware(LOCALES_DIR, I18N_DOMAIN)
    dp.message.middleware(i18n)
    dp.callback_query.middleware(i18n)

    # checking subscription middleware
    check_subs = CheckSubscription()
    dp.message.middleware(check_subs)
    dp.callback_query.middleware(check_subs)

    return i18n, check_subs
