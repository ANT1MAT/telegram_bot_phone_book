from bot import dp
from aiogram import executor
import importlib

importlib.import_module('handler.start')
importlib.import_module('handler.del_data')
importlib.import_module('handler.inline')
importlib.import_module('handler.add_new_data')


if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, skip_updates=True)
