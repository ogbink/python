from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_button = [
    'Continue',
]

confirm_button = [
    '✅ Confirm',
    '💢 Cancel'
]


def phone_markup():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text=phone_button[0], request_contact=True
                )
            ],
        ],
    )
    return keyboard
