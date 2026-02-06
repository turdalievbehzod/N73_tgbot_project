from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardRemove, CallbackQuery

from filters.is_admin import IsAdmin
from keybaords.default.admin import admin_main_menu
from keybaords.default.user import dynamic_reply_keyboard_builder
from keybaords.inline.admin import course_detail_keyboard, CourseCallback
from states.admin import AddCourseState, CourseDetailState
from utils.queries.admin import add_course, get_courses, get_course_by_title, delete_course, update_course_status

router = Router()


async def get_courses_keyboards(message, _, state, locale):
    keyboards = []
    courses = await get_courses()

    for course in courses:
        keyboards.append(course['title'])

    keyboard = KeyboardButton(text=_("➕ Add new course"))
    reply_markup = await dynamic_reply_keyboard_builder(
        keyboards=keyboards, _=_, locale=locale,
        extra_keyboards=[keyboard]
    )
    return reply_markup


@router.message(F.text.in_(['🎓 Courses', '🎓 Курсы', '🎓 Kurslar']), IsAdmin())
async def admin_course_handler(message: types.Message, state: FSMContext, _, locale: str):
    text = _("All courses list")

    reply_markup = await get_courses_keyboards(
        message, _, state, locale
    )
    await message.answer(text=text, reply_markup=reply_markup)
    await state.set_state(CourseDetailState.search)


@router.message(F.text.in_(['➕ Add new course', "➕ Yangi kurs qo'shish", '➕ Add new course']),
                IsAdmin(), CourseDetailState.search)
async def add_course_handler(message: types.Message, state: FSMContext, _):
    text = _("Please enter the image of new course")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())

    await state.set_state(AddCourseState.image)


@router.message(F.photo, AddCourseState.image)
async def get_course_image_handler(message: types.Message, state: FSMContext, _):
    await state.update_data(image=message.photo[-1].file_id)

    text = _("Enter title in uzbek")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddCourseState.title_uz)


@router.message(AddCourseState.title_uz)
async def get_course_title_handler(message: types.Message, state: FSMContext, _):
    await state.update_data(title={
        'uz': message.text
    })

    text = _("Enter title in russian")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddCourseState.title_ru)


@router.message(AddCourseState.title_ru)
async def get_course_title_handler(message: types.Message, state: FSMContext, _):
    data = await state.get_data()
    title = data.get('title')
    title['ru'] = message.text
    await state.update_data(title=title)

    text = _("Enter title in english")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddCourseState.title_en)


@router.message(AddCourseState.title_en)
async def get_course_title_handler(message: types.Message, state: FSMContext, _):
    data = await state.get_data()
    title = data.get('title')
    title['en'] = message.text
    await state.update_data(title=title)

    text = _("Enter description in uzbek")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddCourseState.info_uz)


@router.message(AddCourseState.info_uz)
async def get_course_title_handler(message: types.Message, state: FSMContext, _):
    await state.update_data(info={
        'uz': message.text
    })

    text = _("Enter description in russian")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddCourseState.info_ru)


@router.message(AddCourseState.info_ru)
async def get_course_title_handler(message: types.Message, state: FSMContext, _):
    data = await state.get_data()
    info = data.get('info')
    info['ru'] = message.text
    await state.update_data(info=info)

    text = _("Enter description in english")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddCourseState.info_en)


@router.message(AddCourseState.info_en)
async def get_course_title_handler(message: types.Message, state: FSMContext, _):
    data = await state.get_data()
    info = data.get('info')
    info['en'] = message.text
    await state.update_data(info=info)

    new_data = await state.get_data()

    if await add_course(new_data):
        text = _("✅ Successfully added new course")
    else:
        text = _("❌ Something went wrong, please try again later")

    await message.answer(text=text, reply_markup=await admin_main_menu(_))
    await state.clear()


@router.message(CourseDetailState.search)
async def get_course_handler(message: types.Message, state: FSMContext, _, locale: str):
    course: dict = await get_course_by_title(message.text, locale)
    if course:
        await message.answer_photo(
            photo=course['image'], caption=course['info'][locale],
            reply_markup=await course_detail_keyboard(
                course_id=course['id'], is_active=course['is_active'], _=_
            )
        )


@router.callback_query(CourseDetailState.search, CourseCallback.filter())
async def course_delete_callback_handler(
        call: CallbackQuery,
        callback_data: CourseCallback,
        state: FSMContext,
        _,  # or translator, or gettext, etc.
        locale: str
):
    course_id = callback_data.course_id
    is_active = not callback_data.is_active
    action = callback_data.action

    if action == "delete":
        if await delete_course(course_id=course_id):
            text = "✅ Course is deleted"
            reply_markup = await get_courses_keyboards(
                call.message, _, state, locale
            )
            await call.message.answer(text=text, reply_markup=reply_markup)
            await call.message.delete()
        else:
            text = _("❌ Something went wrong, please try again later")

        await call.answer(text=text, show_alert=True)
    else:
        if await update_course_status(course_id=course_id, status=is_active):
            text = "✅ Course status updated"
            await call.message.edit_reply_markup(
                reply_markup=await course_detail_keyboard(
                    course_id=course_id, is_active=is_active, _=_
                )
            )
        else:
            text = _("❌ Something went wrong, please try again later")

        await call.answer(text=text, show_alert=True)
