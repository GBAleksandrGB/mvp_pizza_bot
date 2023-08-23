from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

from create_bot import dp, bot
from db import sql_start
from keyboards import admin_kb


ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что необходимо сделать???', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото')


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        
        await FSMAdmin.next()
        await message.reply('Теперь введите название')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        
        await FSMAdmin.next()
        await message.reply('Теперь введите описание')


# @dp.message_handler(state=FSMAdmin.name)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        
        await FSMAdmin.next()
        await message.reply('Теперь укажите цену')


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        
        await sql_start.sql_add_command(state)
        await state.finish()


# @dp.message_handler(state='*', commands='Отмена')
# @dp.message_handler(Text(equals('отмена'), ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


# @dp.callback_query_handler(lambda x: x.data and x.data.startswitch('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sql_start.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


# dp.message_handler(commands=['Удалить'])
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sql_start.sql_read_now(message)
        for rst in read:
            await bot.send_photo(message.from_user.id, rst[0], f'{rst[1]}\nОписание: {rst[2]}\nЦена: {rst[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=types.InlineKeyboardMarkup().\
                                   add(types.InlineKeyboardButton(f'Удалить {rst[1]}', callback_data=f'del {rst[1]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)                                                                                                                                                                                                                                                                                      
    dp.register_message_handler(cancel_handler, state='*', commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(del_callback_run, Text(startswith='del '))
    dp.register_message_handler(delete_item, commands=['Удалить'])
