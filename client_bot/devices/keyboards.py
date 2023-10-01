from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_btn = InlineKeyboardButton(text='Назад', callback_data='back')

action_btns = {
    0: [InlineKeyboardButton(text='Включить', callback_data='1')],
    1: [InlineKeyboardButton(text='Выключить', callback_data='0')]
}


def get_devices_keyboard(devices: dict):
    names = []
    for gpio in devices:
        names.append(InlineKeyboardButton(text=gpio, callback_data=devices[gpio]))

    return InlineKeyboardMarkup(inline_keyboard=[names])


def get_device_keyboard(value: int):
    return InlineKeyboardMarkup(inline_keyboard=[action_btns[value]])
