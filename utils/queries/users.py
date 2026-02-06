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


async def add_user(data: dict) -> bool | None:
    try:
        chat_id = data.get('chat_id')
        username = data.get('username')
        language = data.get('language')

        query = "INSERT INTO users (chat_id, username, language) VALUES (%s, %s, %s)"
        params = (chat_id, username, language)
        return execute_query(query=query, params=params)
    except Exception as e:
        logger.error(msg=e)
        return None


async def update_user(data: dict, message: types.Message) -> bool | None:
    try:
        full_name = data.get('full_name')
        phone_number = data.get('phone_number')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        query = ("UPDATE users SET full_name=%s, phone_number=%s, latitude=%s, longitude=%s"
                 " WHERE chat_id=%s")
        params = (full_name, phone_number, latitude, longitude, message.from_user.id,)
        execute_query(query=query, params=params)
        return True
    except Exception as e:
        logger.error(msg=e)
        return None
