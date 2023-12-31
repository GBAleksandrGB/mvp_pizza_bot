import string
import json

from aiogram import types, Dispatcher

from create_bot import dp


# @dp.message_handler()
async def echo_send(message: types.Message):
    words_from_msg = {i.lower().translate(str.maketrans(
        '', '', string.punctuation)) for i in message.text.split(' ')}

    if words_from_msg.intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены!')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
