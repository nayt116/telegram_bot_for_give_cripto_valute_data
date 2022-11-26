import config
from coin_data_pr import Get_Coins
from msg.messages import *

from set_database.SET_db import Connection_to_DB, Set_Table
from aiogram import Dispatcher, types, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled


bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

get_coin = Get_Coins()

# set keyboard
btn1 = types.InlineKeyboardButton('get all coins', callback_data='get_all_coins')
mrk1 = types.InlineKeyboardMarkup(row_width=1)
mrk1.add(btn1)

# set databases
set_tb_users = Set_Table('Cripto_users')
set_tb_admin = Set_Table('Admin_users')
set_tb_ban = Set_Table('Ban_Users')


async def anti_flood(*args, **kwargs):
    msg = args[0]
    user_id = msg.from_user.id
    why = 'flood'
    data_user = {
        'why':why
    }
    #ban user
    set_tb_ban.add(user_id, *data_user.keys(), **data_user)
    await msg.answer(WHY_BLOCKED[0])


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    '''Приветствие'''
    user_id = message.from_user.id

    if set_tb_ban.chek_in('user_id', user_id):
         await message.answer( WHY_BLOCKED[1] )
         print('[OK] Ohh you are blocked!!!')

    elif set_tb_users.chek_in('user_id', user_id):
        if set_tb_admin.chek_in('user_id', user_id):
            await message.answer( GREETING['for_reg_user'].format(message.from_user["first_name"]), reply_markup=mrk1 )
            print('[OK] All right!!!')
        else:
            await message.answer(GREETING['for_reg_user'].format(message.from_user["first_name"]))

    else:
        await message.answer( GREETING['for_not_reg'] )
        print('[OK] Please registered!!!')


@dp.message_handler(commands=['help'], commands_prefix='!/')
async def help(msg: types.Message):
    '''Рассказывает о функиях бота'''
    user_id = msg.from_user.id

    if set_tb_ban.chek_in('user_id', user_id):
        await msg.answer(WHY_BLOCKED[1])
    else:
        await msg.answer(HELP['help'])


@dp.message_handler(commands=['reg'], commands_prefix='!/')
async def registration(msg: types.Message):
    '''Функция регистрации'''
    text = msg.text[5:]
    data = [text.split(',')[i].strip() for i in range(3)]
    user_id = msg.from_user.id
    conn_db = Connection_to_DB()

    if set_tb_users.chek_in('user_id', user_id):
        await bot.send_message(msg.chat.id, REGISTER_USER['for_reg_user'])
    else:
        conn_db.reg(data[0], data[1], data[2], user_id)
        await bot.send_message(msg.chat.id, REGISTER_USER['for_not_reg_user']['now_reging'])
    if set_tb_admin.chek_in('user_id', user_id):
        await msg.answer(ADMIN['ds'], reply_markup=mrk1)
    else:
        await msg.answer(NOT_ADMIN['ds'])


@dp.message_handler(commands=['get_coins'], commands_prefix='!/')
async def get_cripto_coins(message: types.Message):
    '''Функция отправки определённого количества криптовалют'''
    user_id = message.from_user.id
    c = get_coin.get_all_coins()
    f = 0
    l = ''
    if not set_tb_ban.chek_in('user_id', user_id):
        if set_tb_users.chek_in('user_id', user_id):
            if not set_tb_admin.chek_in('user_id', user_id):
                try:
                    value = int(message.text[11:])
                except:
                    await message.answer(GET_COINS['ERROR']['er'])
                for j in c.keys():
                    if value > 10:
                        await message.answer(GET_COINS['for_not_admin']['er_max_value'])
                        break
                    if f == value:
                        break
                    l += f'{j}, {c[j]}\n'
                    f+=1
                try:
                    await message.answer(l)
                except:
                    pass
            else:
                try:
                    value = int(message.text[11:])
                except:
                    await message.answer(GET_COINS['ERROR']['er'])
                for j in c.keys():
                    if f == value:
                        break
                    l += f'{j}, {c[j]}\n'
                    f += 1
                try:
                    await message.answer(l)
                except:
                    pass
        else:
            await message.answer(REGISTER_USER['for_not_reg_user']['make_someone_without_reg'])
    else:
        await message.answer(WHY_BLOCKED[1])


@dp.message_handler(commands=['get_coin'], commands_prefix='!/')
async def get_send_coin(msg: types.Message):
    '''Отправка определённой криптовалюты'''
    user_id = msg.from_user.id

    if not set_tb_ban.chek_in('user_id', user_id):
        try:
            if set_tb_admin.chek_in('user_id', user_id):
                data_coins = get_coin.get_all_coins()
                coin_name = msg.text[10:]
                await msg.answer(ADMIN['use'].format(coin_name, data_coins[coin_name.strip()]))
            else:
                await msg.answer(NOT_ADMIN['use'])
        except KeyError:
            await msg.answer('Вы ввели не правильное название!')
    else:
        await msg.answer(WHY_BLOCKED[1])


@dp.message_handler(commands=['get_all_coins'], commands_prefix='!/')
async def get_all_coins_inl_btn1(msg: types.Message):
    '''Отправка всех криптовалют'''
    data = get_coin.get_all_coins()
    user_id = msg.from_user.id
    l = ''
    if not set_tb_ban.chek_in('user_id', user_id):
        if set_tb_users.chek_in('user_id', user_id):
            if set_tb_admin.chek_in('user_id', user_id):
                for i in data.keys():
                    l += f'{i}:  {data[i]}\n'
                try:
                    await msg.answer(l)
                except:
                    pass
        else:
            await msg.answer(REGISTER_USER['for_not_reg_user']['make_someone_without_reg'])
    else:
        await msg.answer(WHY_BLOCKED[1])


@dp.callback_query_handler(lambda c: c.data == 'get_all_coins')
async def get_all_coins_inl_btn2(call: types.CallbackQuery):
    data = get_coin.get_all_coins()
    user_id = call.from_user.id
    l = ''
    if not set_tb_ban.chek_in('user_id', user_id):
        if set_tb_users.chek_in('user_id', user_id):
            if set_tb_admin.chek_in('user_id', user_id):
                for i in data.keys():
                    l += f'{i}:  {data[i]}\n'
                try:
                    await call.message.answer(l)
                except:
                    pass
        else:
            await call.message.answer(REGISTER_USER['for_not_reg_user']['make_someone_without_reg'])
    else:
        await call.message.answer(WHY_BLOCKED[1])


@dp.message_handler()
@dp.throttled(anti_flood, rate=0.5)
async def chek_flood(msg: types.Message):
    '''Анти спам'''
    user_id = msg.from_user.id
    if set_tb_ban.chek_in('user_id', user_id):
        await msg.reply(WHY_BLOCKED[1])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)