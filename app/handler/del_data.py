import sqlite3
from handler.inline import execute_read_query
from bot import dp, bot, Del_data
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


@dp.callback_query_handler(lambda c: c.data == 'del_shop')
async def del_shop(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите название точки', reply_markup=ReplyKeyboardRemove())
    await Del_data.shop_name.set()


@dp.message_handler(state=Del_data.shop_name)
async def send_shop_list(message: types.Message, state: FSMContext):
    connection = sqlite3.connect('db_python_app.sqlite')
    query = "SELECT * FROM Numbers WHERE UPPER(Shop) LIKE '%{}%'".format(message.text)
    results = execute_read_query(connection, query)
    respons = ReplyKeyboardMarkup()
    for result in results:
        button = KeyboardButton(text=result[0])
        respons.add(button)
    await Del_data.del_data.set()
    await bot.send_message(message.from_user.id, 'Какую из этих точек вы хотите удалить?',
                           reply_markup=respons)


@dp.message_handler(state=Del_data.del_data)
async def send_shop_list(message: types.Message, state: FSMContext):
    await message.answer('Точка {} удалена.'.format(message.text), reply_markup=ReplyKeyboardRemove())
    connection = sqlite3.connect('db_python_app.sqlite')
    cur = connection.cursor()
    query = "DELETE FROM Numbers WHERE Shop = '{}';".format(message.text)
    cur.execute(query)
    connection.commit()
    await state.finish()