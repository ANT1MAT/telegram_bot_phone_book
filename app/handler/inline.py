import sqlite3
from sqlite3 import Error
from bot import dp, bot
from aiogram.types import InlineQueryResultArticle, InputContactMessageContent
from aiogram.types.inline_query import InlineQuery


#Функция для обработки SQL запроса к БД
def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


#инлайн режим
@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query.capitalize()
    connection = sqlite3.connect('db_python_app.sqlite')
    query = "SELECT * FROM Numbers WHERE UPPER(Shop) LIKE '%{}%'".format(text)
    results = execute_read_query(connection, query)
    respons = []
    i = 0
    for result in results:
        item = InlineQueryResultArticle(
            id=str(i),
            title=result[0],
            description=result[1],
            input_message_content=InputContactMessageContent(first_name=result[0],
                                                             phone_number=result[1]))
        respons.append(item)
        i += 1
    await bot.answer_inline_query(inline_query.id, results=respons, cache_time=1)