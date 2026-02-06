import logging

from psycopg2.extras import Json

from core.db_settings import execute_query

logger = logging.getLogger(__name__)


async def add_course(data: dict) -> bool | None:
    try:
        image = data.get('image')
        title = Json(data.get('title'))
        info = Json(data.get('info'))

        query = "INSERT INTO courses (image, title, info) VALUES (%s, %s, %s)"
        params = (image, title, info)
        return execute_query(query=query, params=params)
    except Exception as e:
        logger.error(msg=e)
        return None


async def get_courses(status: bool = None) -> dict | None:
    """
    Get all active courses
    :param status: course status
    :return: user data or None
    """
    try:
        if status is None:
            query = "SELECT * FROM courses"
            params = None
        else:
            query = "SELECT * FROM courses WHERE is_active = %s"
            params = (status,)
        courses = execute_query(query=query, params=params, fetch="all")
        return courses
    except Exception as e:
        logger.error(msg=e)
        return None


async def get_course_by_title(title: str, locale: str) -> dict | None:
    try:
        query = """
                SELECT *
                FROM courses
                WHERE title ->> %s = %s \
                """
        params = (locale, title)

        courses = execute_query(
            query=query,
            params=params,
            fetch="one"
        )
        return courses

    except Exception as e:
        logger.error(msg=e)
        return None


async def delete_course(course_id: int) -> bool | None:
    try:
        query = "DELETE FROM courses WHERE id=%s"
        params = (course_id,)

        execute_query(query=query, params=params)
        return True
    except Exception as e:
        logger.error(msg=e)
        return None


async def update_course_status(course_id: int, status: bool) -> bool | None:
    try:
        query = ("UPDATE courses SET is_active=%s WHERE id=%s")
        params = (status, course_id,)
        execute_query(query=query, params=params)
        return True
    except Exception as e:
        logger.error(msg=e)
        return None
