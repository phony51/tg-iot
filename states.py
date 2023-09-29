from aiogram.fsm.state import StatesGroup, State


class DevicesManagerStates(StatesGroup):
    device_information = State()
    device_actions = State()
