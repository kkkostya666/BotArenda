import re

from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from state import UserState
from keyboards.inline.start import get_start_keyboard, get_order_keyboard, get_order_keyboard_user, get_sity_keyboard, \
    get_1_keyboard, get_2_keyboard
from aiogram import F
from bd import Db

router = Router()
bd = Db()
current_index = 0
index = 0
index_1 = 0


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text="<i>Добро пожаловать в бота!</i>\n<b>Здесь вы можете забронировать квартиру в Казани</b>",
                         reply_markup=await get_start_keyboard())


@router.callback_query(F.data == "create_kv")
async def create_order(callback: types.CallbackQuery):
    global current_index
    results = bd.select_home()
    if results:
        result = results[current_index]
        formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
        await callback.message.answer(formatted_text, reply_markup=await get_order_keyboard())
    else:
        await callback.message.answer("No data available")


@router.callback_query(F.data == "next")
async def create_order(callback: types.CallbackQuery):
    global current_index
    current_index += 1
    results = bd.select_home()
    if results and current_index < len(results):
        result = results[current_index]
        formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
        await callback.message.edit_text(formatted_text, reply_markup=await get_order_keyboard())
    else:
        current_index = 0
        results = bd.select_home()
        if results:
            result = results[current_index]
            formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
            await callback.message.edit_text(formatted_text, reply_markup=await get_order_keyboard())
        else:
            await callback.message.edit_text("No data available")


@router.callback_query(F.data == "create_order")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message.text
    address_pattern = re.compile(r"📍 Адрес: (.+)")
    address_match = address_pattern.search(message)
    if address_match:
        full_address = address_match.group(1).strip()
        await state.update_data(address=full_address)
    else:
        print("Адрес не найден в сообщении.")
    await callback.message.answer(text="Введите дату на которое хотите забронировать\n\n<i>Пример: 30.05</i>")
    await state.set_state(UserState.date)


@router.message(UserState.date)
async def floor(msg: types.Message, state: FSMContext):
    date = msg.text
    await state.update_data(date=date)
    username = msg.from_user.username
    user = bd.select_user(username)
    user_result = user[0][0]
    data = await state.get_data()
    address = data['address']
    result = bd.select_home_name(address)
    if result:
        home_id = result[0][0]
        try:
            status = "🕐 На рассмотрении"
            bd.insert_into_orders(home_id, user_result, data['date'], status)
            await msg.answer(
                "<b>Квартира предварителньо забронирована! Дождитесь ответа менеджера</b>\n\n<i>Статус: 🕐 На рассмотрении</i>",
                reply_markup=await get_order_keyboard_user())
            await state.clear()
        except ValueError as e:
            await msg.answer(f"К сожалению на эту дату квартира уже забронирована.")
    else:
        await msg.answer("Дом с таким адресом не найден")


@router.callback_query(F.data == "my")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    username = callback.from_user.username
    result = bd.select_orders_by_username(username)
    if result:
        message_text = "<i>Ваши заказы:</i>\n"
        for row in result:
            order_id, address, date, status = row
            message_text += f"<b>ID заказа:</b> {order_id}, <b>Адрес:</b> {address}, <b>Дата:</b> {date}, <b>Статус:</b> {status}\n\n"
    else:
        message_text = "У вас нет заказов."
    await callback.message.answer(text=message_text)


@router.callback_query(F.data == "support")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="<i>Ниже представлены все доступные районы Казани</i>",
                                  reply_markup=await get_sity_keyboard())


@router.callback_query(F.data == "1")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    global index
    results = bd.select_home_by_address("Приволжский")
    if results:
        result = results[index]
        formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
        await callback.message.answer(formatted_text, reply_markup=await get_1_keyboard())
    else:
        await callback.message.answer("No data available")


@router.callback_query(F.data == "2")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    global current_index
    results = bd.select_home_by_address("Новосавинский")
    if results:
        result = results[current_index]
        formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
        await callback.message.answer(formatted_text, reply_markup=await get_2_keyboard())
    else:
        await callback.message.answer("No data available")


@router.callback_query(F.data == "next_1")
async def create_order(callback: types.CallbackQuery):
    global index
    index += 1
    results = bd.select_home_by_address("Приволжский")
    if results and index < len(results):
        result = results[index]
        formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
        await callback.message.edit_text(formatted_text, reply_markup=await get_1_keyboard())
    else:
        index = 0
        results = bd.select_home_by_address("Приволжский")
        if results:
            result = results[index]
            formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
            await callback.message.edit_text(formatted_text, reply_markup=await get_1_keyboard())
        else:
            await callback.message.edit_text("No data available")

@router.callback_query(F.data == "next_2")
async def create_order(callback: types.CallbackQuery):
    global index_1
    index_1 += 1
    results = bd.select_home_by_address("Новосавинский")
    if results and index_1 < len(results):
        result = results[index_1]
        formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
        await callback.message.edit_text(formatted_text, reply_markup=await get_2_keyboard())
    else:
        index_1 = 0
        results = bd.select_home_by_address("Новосавинский")
        if results:
            result = results[index_1]
            formatted_text = f"📍 <b>Адрес:</b> <i>{result[1]}</i>\n\n{result[4]}\n<b>{result[2]} квадратных метров</b>\n💰 <b>Цена:</b> {result[3]}"
            await callback.message.edit_text(formatted_text, reply_markup=await get_2_keyboard())
        else:
            await callback.message.edit_text("No data available")