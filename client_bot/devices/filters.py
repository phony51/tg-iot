from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


# class IsValidDevice(BaseFilter):
#     def __init__(self, devices: list[str]):
#         self.devices = devices
#
#     async def __call__(self, cb: CallbackQuery):
#         return self.devices

class GoneBack(BaseFilter):
    async def __call__(self, cb: CallbackQuery):
        return cb.data == 'back'
