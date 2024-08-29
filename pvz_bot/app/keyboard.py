from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def base(data: dict):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(data["date"]), callback_data="date"), InlineKeyboardButton(text=str(data["park"]), callback_data="park"), InlineKeyboardButton(text=str(data["habr"]), callback_data="habr")],
            [InlineKeyboardButton(text=str(data["che1"]), callback_data="che1"), InlineKeyboardButton(text=str(data["che2"]), callback_data="che2"), InlineKeyboardButton(text=str(data["izml"]), callback_data="izml")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="complete")],
        ]
    )