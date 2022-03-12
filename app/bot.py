import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#Кнопки взаимодействия
create_db = InlineKeyboardButton('Настроить бота', callback_data='settings')
first_start_kb = InlineKeyboardMarkup().add(create_db)

add_shop = InlineKeyboardButton('Добавить магазин в БД', callback_data='add_shop')
del_shop = InlineKeyboardButton('Удалить магазин из БД', callback_data='del_shop')
start_kb = InlineKeyboardMarkup().add(add_shop).add(del_shop)


#Состояния
class Password(StatesGroup):
    new_pass_1 = State()
    new_pass_2 = State()
    wait_file = State()


class Add_data(StatesGroup):
    shop_name = State()
    shop_phone = State()


class Del_data(StatesGroup):
    shop_name = State()
    del_data = State()