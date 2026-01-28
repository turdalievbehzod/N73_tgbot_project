from core import models
from core.db_settings import execute_query


async def create_tables():
    execute_query(query=models.users)