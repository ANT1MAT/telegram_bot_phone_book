import sqlite3
from bot import dp, bot, Add_data
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == 'add_shop')
async def add_shop(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите название новой точки')
    await Add_data.shop_name.set()


@dp.message_handler(state=Add_data.shop_name)
async def save_shop_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, 'Ввведите номер новой точки')
    await Add_data.next()


@dp.message_handler(state=Add_data.shop_phone)
async def add_shop(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await Add_data.next()
    data = await state.get_data()
    connection = sqlite3.connect('db_python_app.sqlite')
    cur = connection.cursor()
    query = "SELECT EXISTS (SELECT 1 FROM Numbers WHERE Shop = {})".format(data['name'])
    if cur.execute(query).fetchone()[0]:
        await bot.send_message(message.from_user.id, 'Точка уже существует')
        return await state.finish()
    query = "SELECT EXISTS (SELECT 1 FROM Numbers WHERE Number = '%{}%')".format(data['phone'])
    if cur.execute(query).fetchone()[0]:
        await bot.send_message(message.from_user.id, 'Номер уже привязан к другой точке')
        return await state.finish()
    cur.execute("INSERT INTO Numbers (Shop, Number) VALUES (?,?);", (data['name'], data['phone']))
    connection.commit()
    await bot.send_message(message.from_user.id, 'Точка добавлена')