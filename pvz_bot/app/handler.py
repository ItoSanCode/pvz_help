from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import base_data, db

import app.keyboard as kb

router = Router()


class SearchState(StatesGroup):
    message = State()


class DataState(StatesGroup):
    date = State()
    park = State()
    habr = State()
    che1 = State()
    che2 = State()
    izml = State()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.reply('Привет, пожалуйста введите /help !')


@router.message(Command("help"))
async def start_cmd(message: types.Message):
    await message.reply('Помощь по командам:\n\n/add - добавить новый столбик в базу данных\n/search - поиск по базе данных')


@router.message(Command("add"))
async def add_cmd(message: types.Message, state: FSMContext):
    data = base_data
    await message.answer('Выберите действие', reply_markup=kb.base(data))
    await state.set_data(data=data)


@router.message(Command("search"))
async def search_cmd(message: types.Message, state: FSMContext):
    await message.answer('Введите две даты через тире, пример:\n19:03-25:03')
    await state.set_state(SearchState.message)


@router.message(SearchState.message)
async def search(message: types.Message, state: FSMContext):
    if not message.text.count(":") == 2:
        await message.answer("Ошибка, введите снова")
        return
    if not "-" in message.text:
        await message.answer("Ошибка, введите снова")
        return
    if not len(message.text) == 11:
        await message.answer("Ошибка, введите снова")
        return
    dates = message.text.split("-")
    date0 = dates[0].split(":")
    date1 = dates[1].split(":")
    date0 = {"day": int(date0[0]), "moonth": int(date0[1])}
    date1 = {"day": int(date1[0]), "moonth": int(date1[1])}
    m = await message.answer("⏳ Начинаю поиск")
    result = db.search_data(date0, date1)
    await m.edit_text("✅ Вот что я нашел:")
    for data in result:
        await message.answer(f"🕝 Дата: {data[0].replace(":", ".")}\n\n🏪 PARK: {data[1]}\n🏪 HABR: {data[2]}\n🏪 CHE1: {data[3]}\n🏪 CHE2: {data[4]}\n🏪 IZML: {data[5]}")
    await state.clear()


@router.callback_query(F.data == "complete")
async def complete(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        return
    status = all(isinstance(value, int) for key, value in data.items() if key != "date") and isinstance(data["date"], str)
    if not status:
        await callback.message.answer(f"Вы не заполнили все данные!")
        return
    db.new_data(data)
    await callback.message.answer(f"Столбец был успешно добавлен в таблицу!")


@router.callback_query()
async def complete(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        return
    await callback.answer(".")
    await callback.message.answer(f"Введите {callback.data}")
    await state.set_state(eval(f"DataState.{callback.data}"))


@router.message(DataState.date)
async def date(message: types.Message, state: FSMContext):
    if not len(message.text) == 5:
        await message.answer("Ошибка, введите снова")
        return
    if not ":" in message.text:
        await message.answer("Ошибка, введите снова")
        return

    data = await state.get_data()
    data["date"] = message.text
    await message.answer('Выберите действие', reply_markup=kb.base(data))
    await state.clear()
    await state.set_data(data=data)


@router.message(DataState.park)
async def park(message: types.Message, state: FSMContext):
    try:
        num = int(message.text)
    except:
        await message.answer("Ошибка, введите снова")
        return

    data = await state.get_data()
    data["park"] = num
    await message.answer('Выберите действие', reply_markup=kb.base(data))
    await state.clear()
    await state.set_data(data=data)


@router.message(DataState.habr)
async def habr(message: types.Message, state: FSMContext):
    try:
        num = int(message.text)
    except:
        await message.answer("Ошибка, введите снова")
        return

    data = await state.get_data()
    data["habr"] = num
    await message.answer('Выберите действие', reply_markup=kb.base(data))
    await state.clear()
    await state.set_data(data=data)


@router.message(DataState.che1)
async def che1(message: types.Message, state: FSMContext):
    try:
        num = int(message.text)
    except:
        await message.answer("Ошибка, введите снова")
        return

    data = await state.get_data()
    data["che1"] = num
    await message.answer('Выберите действие', reply_markup=kb.base(data))
    await state.clear()
    await state.set_data(data=data)


@router.message(DataState.che2)
async def che2(message: types.Message, state: FSMContext):
    try:
        num = int(message.text)
    except:
        await message.answer("Ошибка, введите снова")
        return

    data = await state.get_data()
    data["che2"] = num
    await message.answer('Выберите действие', reply_markup=kb.base(data))
    await state.clear()
    await state.set_data(data=data)


@router.message(DataState.izml)
async def izml(message: types.Message, state: FSMContext):
    try:
        num = int(message.text)
    except:
        await message.answer("Ошибка, введите снова")
        return

    data = await state.get_data()
    data["izml"] = num
    await message.answer('Выберите действие', reply_markup=kb.base(data))
    await state.clear()
    await state.set_data(data=data)