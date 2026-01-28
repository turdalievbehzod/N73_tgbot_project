from aiogram import Router

from . import start


def include_routers():
    main_router = Router()
    main_router.include_router(start.router)

    return main_router
