import logging

from aiogram import types

from core.db_settings import execute_query

logger = logging.getLogger(__name__)


async def get_user(chat_id: int) -> dict | None:
    """
    Get user from database by chat_id
    :param chat_id: user id in telegram
    :return: user data or None
    """
    try:
        query = "SELECT * FROM users WHERE chat_id = %s"
        params = (chat_id,)
        user = execute_query(query=query, params=params, fetch="one")
        return user
    except Exception as e:
        logger.error(msg=e)
        return None


async def add_user(data: dict, message: types.Message) -> bool | None:
    try:
        query = ("INSERT INTO users (chat_id, username, language, full_name,"
                 " phone_number, longitude, latitude) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                 )
        params = (message.from_user.id, message.from_user.username, data.get('language'),
                  data.get('full_name'), data.get('phone_number'), data.get('longitude'),
                  data.get('latitude'),
                  )

        return execute_query(query=query, params=params)
    except Exception as e:
        logger.error(msg=e)
        return None