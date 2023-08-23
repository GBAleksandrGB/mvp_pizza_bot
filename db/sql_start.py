import sqlite3 as sq

from aiogram import types

from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('pizza_db')
    cur = base.cursor()

    if base:
        print('Подключение к БД выполнено')
    
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY_KEY, description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message: types.Message):
    for rst in cur.execute("SELECT * FROM menu").fetchall():
        await bot.send_photo(message.from_user.id, rst[0], f'{rst[1]}\nОписание: {rst[2]}\nЦена: {rst[-1]}')


async def sql_read_now(message: types.Message):
    return cur.execute("SELECT * FROM menu").fetchall()


async def sql_delete_command(data):
    cur.execute("DELETE FROM menu WHERE name == ?", (data,))
    base.commit()
