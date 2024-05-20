from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from state import UserState
from bd import Db

from keyboards.inline.start import get_admin_keyboard
from aiogram import F

router = Router()
bd = Db()

ALLOWED_USER_ID = "1383157406"


@router.message(Command("admin"))
async def dispetcher_command(message: types.Message):
    if str(message.from_user.id) == ALLOWED_USER_ID:
        await message.answer("<i>Вы успешно вошли как диспетчер</i>", reply_markup=await get_admin_keyboard(),
                             parse_mode="HTML")
    else:
        await message.answer("Вы не являетесь диспетчером!")


@router.callback_query(F.data == "zayvka")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    result = bd.select_all_orders_with_details()
    message_text = "<i>Все заказы:</i>\n"
    for row in result:
        order_id, address, date, username, status = row
        message_text += f"<b>Дата:</b> {username}, <b>ID заказа:</b> {order_id}, <b>Адрес:</b> {address}, <b>Пользователь:</b> @{date}, <b>Статус:</b> {status}\n\n"
    await callback.message.answer(text=message_text)


@router.message(Command("good_status"))
async def update_status_command(message: types.Message):
    if str(message.from_user.id) == ALLOWED_USER_ID:
        text = message.text
        args = text.split()[1:]
        order_id = args[0]
        status = "Одобрено ✔️"
        if order_id:
            bd.update_order_status(order_id, status)
            await message.answer(f"<b>ID заказа:</b> {order_id}\n<b>Статус:</b> {status}.")
        else:
            await message.answer("Пользователь с таким именем не найден.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")


@router.message(Command("block"))
async def update_status_command(message: types.Message):
    if str(message.from_user.id) == ALLOWED_USER_ID:
        text = message.text
        args = text.split()[1:]
        order_id = args[0]
        status = "Не одобрено ⛔️"
        if order_id:
            bd.update_order_status(order_id, status)
            await message.answer(f"<b>ID заказа:</b> {order_id}\n<b>Статус:</b> {status}.")
        else:
            await message.answer("Пользователь с таким именем не найден.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")