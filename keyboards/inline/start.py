from aiogram import types


async def get_start_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Каталог квартир",
                callback_data="create_kv"
            ),
            types.InlineKeyboardButton(
                text="Каталог по районам",
                callback_data="support"
            ),
            types.InlineKeyboardButton(
                text="Мои заявки",
                callback_data="my"
            )
        ]]
    )


async def get_order_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Забронировать ✔️",
                callback_data="create_order"
            ),
            types.InlineKeyboardButton(
                text="Следующая ➡️",
                callback_data="next"
            ),
        ]]
    )


async def get_order_keyboard_user():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Мои заявки",
                callback_data="my"
            )
        ]]
    )


async def get_admin_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Управлять заявками",
                callback_data="zayvka"
            )
        ]]
    )


async def get_sity_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Приволжский",
                callback_data="1"
            ),
            types.InlineKeyboardButton(
                text="Новосавинский",
                callback_data="2"
            ),
        ]]
    )


async def get_1_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Забронировать ✔️",
                callback_data="create_order"
            ),
            types.InlineKeyboardButton(
                text="Следующая ➡️",
                callback_data="next_1"
            ),
        ]]
    )
async def get_2_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Забронировать ✔️",
                callback_data="create_order"
            ),
            types.InlineKeyboardButton(
                text="Следующая ➡️",
                callback_data="next_2"
            ),
        ]]
    )