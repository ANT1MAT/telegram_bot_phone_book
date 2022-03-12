import os
import pandas
import sqlite3
from bot import dp, bot, Password, start_kb, first_start_kb
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if os.path.exists('db_python_app.sqlite'):
        await message.answer(f'Привет, {message.from_user.full_name}.', reply_markup=start_kb)
    else:
        await message.answer(f'Привет, {message.from_user.full_name}, это первый запуск бота.', reply_markup=first_start_kb)


# Настройка бота
@dp.callback_query_handler(lambda c: c.data == 'settings')
async def create_db(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Введите пароль администратора')
    await bot.answer_callback_query(callback_query.id)
    await Password.new_pass_1.set()


@dp.message_handler(state=Password.new_pass_1)
async def take_pass_1(message: types.Message, state: FSMContext):
    await state.update_data(pass_1=message.text)
    await bot.send_message(message.from_user.id, 'Повторите пароль')
    await Password.next()

@dp.message_handler(state=Password.new_pass_2)
async def take_pass_1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['pass_1'] == message.text:
        await bot.send_message(message.from_user.id, 'Пароли совпадают')
        await bot.send_message(message.from_user.id, f'Ваш пароль: {data["pass_1"]}')
        await bot.send_message(message.from_user.id, 'Отправьте файл со списком магазинов')
        await Password.wait_file.set()
    else:
        await bot.send_message(message.from_user.id, 'Пароли не совпали, повторите ввод пароля')


# получение эксель файла для БД
@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=Password.wait_file)
async def save_file(message: types.Message, state: FSMContext):
    file = await bot.get_file(message.document.file_id)
    await file.download(destination_file='base.xlsx')
    await message.answer('Файл получен')
    connection = sqlite3.connect('db_python_app.sqlite')
    data = pandas.read_excel(r'base.xlsx', index_col=0)
    data.to_sql("Numbers", con=connection)
    os.remove('base.xlsx')
    await message.answer('БД создана')
    await state.finish()


#Ответ бота, если получено сообщение, а не файл
@dp.message_handler(state=Password.wait_file)
async def ti_tupoy(message: types.Message):
    await bot.send_message(message.from_user.id, 'Отправьте xlsx файл для БД')