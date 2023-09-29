from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from controller_api import ControllerAPI
from keyboards import devices_kb, get_device_keyboard
from states import DevicesManagerStates

devices_router = Router()


def format_device_info(value: int):
    return 'Состояние устройства: {value}'.format(value={1: 'Включено', 0: 'Выключено'}.get(value, 'Неизвестно'))


async def edit_device_info(msg: Message, value: int):
    await msg.edit_text(format_device_info(value), reply_markup=get_device_keyboard(value))


@devices_router.message(Command('start'))
async def start(msg: Message, state: FSMContext):
    await msg.reply('Выберите устройство:', reply_markup=devices_kb)
    await state.set_state(DevicesManagerStates.device_information)


@devices_router.callback_query(DevicesManagerStates.device_information)
async def device_info(cb: CallbackQuery, state: FSMContext, controller: ControllerAPI):
    value = controller.get_out(cb.data)
    await state.update_data(current_gpio=cb.data)
    await edit_device_info(cb.message, value)
    await state.set_state(DevicesManagerStates.device_actions)


@devices_router.callback_query(DevicesManagerStates.device_actions)
async def device_action(cb: CallbackQuery, state: FSMContext, controller: ControllerAPI):
    data = await state.get_data()
    value = int(cb.data)
    controller.set_out(data['current_gpio'], value)
    await edit_device_info(cb.message, value)
