from aiogram.fsm.state import StatesGroup, State


class AddCourseState(StatesGroup):
    image = State()
    title_uz = State()
    title_ru = State()
    title_en = State()
    info_uz = State()
    info_ru = State()
    info_en = State()


class CourseDetailState(StatesGroup):
    search = State()
