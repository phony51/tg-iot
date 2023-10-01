from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from .keyboards import get_devices_keyboard, get_device_keyboard
from .middlewares import ControllerAPIInjection
from .states import DevicesManagerStates
from controller_api import ControllerAPI

devices_router = Router()
devices_router.message.outer_middleware(ControllerAPIInjection())
devices_router.callback_query.outer_middleware(ControllerAPIInjection())


def format_device_info(value: int):
    return 'Состояние устройства: {value}'.format(value={1: 'Включено', 0: 'Выключено'}.get(value, 'Неизвестно'))


async def edit_device_info(msg: Message, value: int):
    await msg.edit_text(format_device_info(value), reply_markup=get_device_keyboard(value))


@devices_router.message(Command('start'))
async def start(msg: Message, state: FSMContext, controller_client: ControllerAPI):
    await msg.reply('Выберите устройство:', reply_markup=get_devices_keyboard(controller_client.get_devices()))
    await state.set_state(DevicesManagerStates.device_information)


@devices_router.callback_query(DevicesManagerStates.device_information)
async def device_info(cb: CallbackQuery, state: FSMContext, controller_client: ControllerAPI):
    value = controller_client.get_out(cb.data)
    await state.update_data(current_gpio=cb.data)
    await edit_device_info(cb.message, value)
    await state.set_state(DevicesManagerStates.device_actions)


@devices_router.callback_query(DevicesManagerStates.device_actions)
async def device_action(cb: CallbackQuery, state: FSMContext, controller_client: ControllerAPI):
    data = await state.get_data()
    value = int(cb.data)
    controller_client.set_out(data['current_gpio'], value)
    await edit_device_info(cb.message, value)
