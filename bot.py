import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import random
import pandas as pd

df_dr = pd.read_excel('konstruktor_dr.xlsx')
df_ng = pd.read_excel('konstruktor_ng.xlsx')

bot = Bot(token='6065678394:AAGHSZBgv4P_ovtMKtEJVMI9v3gSDbyycdY', proxy="http://proxy.server:3128")  # создаю бота и указываю его токен
logging.basicConfig(level=logging.INFO)                            # включаю логирование, чтоб не упустить ошибки
dp = Dispatcher(bot)                                               # считыватель переписки с ботом (диспетчер)
cb = CallbackData('filter', 'option', 'action')

bud = ' '
pust = ' '
sdr = ' '
gelau = ' '

sng = ' '
yagelau = ' '
ipust = ' '


info_text = 'Для начала выбери, с каким праздником хочешь поздравить:\n' 'Для этого введи команду /new_year для поздравления с Новым годом!\n' 'или /happy_birthday для поздравления с Днем рождения!\n'

@dp.message_handler(commands=['info', 'menu'])                    # текст с информацией
async def info(message):
    await message.answer(info_text)

@dp.message_handler(commands=['start', 'help'])                    # Главное меню с информацией
async def print_hi(message):
    await message.answer('Привет!\n'
                         'Меня зовут Лися.\n'
                         'Я бот, который поможет тебе составить поздравление\n')
    keyboard_hi = InlineKeyboardMarkup()
    buttons_hi = [InlineKeyboardButton(text='Привет! Хорошо!', callback_data=cb.new(option='Хорошо', action='hi')),
    InlineKeyboardButton(text='Привет! Не очень...', callback_data=cb.new(option='Не очень', action='hi'))]
    keyboard_hi.add(*buttons_hi)
    await message.answer('Как твоё настроение?', reply_markup=keyboard_hi)

@dp.message_handler(commands=['happy_birthday'])                    # С Днем рождения
async def happy_birthday(message):
    global sdr, gelau, bud, pust
    sdr = ' '
    gelau = ' '
    bud = ' '
    pust = ' '
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEIihZkNRn7duSrhDbkm9uTCsDJrtE7tgAC-yoAAtTxeEmQKzJHE8WeIC8E')
    await message.answer(hb_sdr_text() + '...')
    keyboard_sdr = InlineKeyboardMarkup()
    buttons_sdr = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='С ДР', action='hi')),
                  InlineKeyboardButton(text='Дальше\n', callback_data=cb.new(option='Желаю', action='hi'))]
    keyboard_sdr.add(*buttons_sdr)
    await message.answer('\nПродолжим?', reply_markup=keyboard_sdr)

@dp.message_handler(commands=['new_year'])                    # С Новым годом
async def new_year(message):
    global sng, yagelau, ipust
    sng = ' '
    yagelau = ' '
    ipust = ' '
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEIqn5kQjrp6E2df_webm4d7zuy0POfPgACIiUAAu-CeUncy409nLgYUC8E')
    await message.answer(hb_sng_text())
    keyboard_sng = InlineKeyboardMarkup()
    buttons_sng = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='С НГ', action='hi')),
                  InlineKeyboardButton(text='Дальше\n', callback_data=cb.new(option='Некст_нг', action='hi')),
                  InlineKeyboardButton(text='Стоп. Полное поздравление\n', callback_data=cb.new(option='Текст_нг', action='hi'))]
    keyboard_sng.add(*buttons_sng)
    await message.answer('\nПродолжим?', reply_markup=keyboard_sng)

#Генерирую рандомные поздравления
def hb_sdr_text():
    global sdr
    sdr = random.choice(df_dr['С Днем рождения!'])
    sdr = 'С Днем рождения! '+str(sdr)
    return (sdr)

def hb_gelau_text():
    global gelau
    gelau = random.choice(df_dr['желаю'])
    gelau = 'желаю '+str(gelau)
    return (gelau)

def hb_bud_text():
    global bud
    bud = random.choice(df_dr['Будь'])
    bud = 'Будь '+str(bud)
    return (bud)

def hb_pust_text():
    global pust
    pust = random.choice(df_dr['И пусть'])
    pust = 'И пусть '+str(pust)
    return (pust)

def hb_sng_text():
    global sng
    sng = random.choice(df_ng['С новым годом!'])
    sng = 'С Новым годом! '+str(sng)
    return (sng)

def hb_yagelau_text():
    global yagelau
    yagelau = random.choice(df_ng['Я желаю'])
    yagelau = 'Я желаю'+str(yagelau)
    return (yagelau)

def hb_ipust_text():
    global ipust
    ipust = random.choice(df_ng['И пусть'])
    ipust = 'И пусть '+str(ipust)
    return (ipust)

@dp.callback_query_handler(cb.filter())  #все кнопки
async def set_button_hi(call, callback_data):
    if callback_data['option'] == 'Хорошо':
        await bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEIiVlkNPtNnzlIZj7Uc7VzKcl3kWUtTQACtCwAAoXveElb73hw0iBfEy8E')           #Отправка стикера
        await call.message.answer('Замечательно!\n' + str(info_text))

    elif callback_data['option'] == 'Не очень':
        await bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEIiZpkNQgw0dzqUMCXfRsLrfcAASzlxRIAAr4oAAKqYHlJgmFIgvohYosvBA')
        await call.message.answer('Надеюсь, что смогу его улучшить!\n' + str(info_text))

    elif callback_data['option'] == 'С ДР':
        await call.message.answer(hb_sdr_text() + '...')
        keyboard_sdr = InlineKeyboardMarkup()
        buttons_sdr = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='С ДР', action='hi')),
                      InlineKeyboardButton(text='Дальше\n', callback_data=cb.new(option='Желаю', action='hi'))]
        keyboard_sdr.add(*buttons_sdr)
        await call.message.answer('\nПродолжим?', reply_markup=keyboard_sdr)

    elif callback_data['option'] == 'Желаю':
        await call.message.answer(hb_gelau_text())
        keyboard_gelau = InlineKeyboardMarkup()
        buttons_gelau = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='Желаю', action='hi')),
                         InlineKeyboardButton(text='Стоп. Полное поздравление\n', callback_data=cb.new(option='Текст_др', action='hi')),
                         InlineKeyboardButton(text='Дальше\n', callback_data=cb.new(option='Некст', action='hi'))]
        keyboard_gelau.add(*buttons_gelau)
        await call.message.answer('\nПродолжим?', reply_markup=keyboard_gelau)

    elif callback_data['option'] == 'Некст':
        keyboard_hb = InlineKeyboardMarkup()
        buttons_hb = [InlineKeyboardButton(text='Будь ...\n', callback_data=cb.new(option='Будь', action='hi')),
                      InlineKeyboardButton(text='И пусть...\n', callback_data=cb.new(option='пусть', action='hi'))]
        keyboard_hb.add(*buttons_hb)
        await call.message.answer('Как продолжим поздравление?', reply_markup=keyboard_hb)

    elif callback_data['option'] == 'Будь':
        await call.message.answer(hb_bud_text())
        keyboard_bud = InlineKeyboardMarkup()
        buttons_bud = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='Будь', action='hi')),
                      InlineKeyboardButton(text='Стоп. Полное поздравление', callback_data=cb.new(option='Текст_др', action='hi')),
                      InlineKeyboardButton(text='Дальше\n', callback_data=cb.new(option='пусть', action='hi'))]
        keyboard_bud.add(*buttons_bud)
        await call.message.answer('\nПродолжим?', reply_markup=keyboard_bud)

    elif callback_data['option'] == 'пусть':
        await call.message.answer(hb_pust_text())
        keyboard_pust = InlineKeyboardMarkup()
        buttons_pust = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='пусть', action='hi')),
                      InlineKeyboardButton(text='Стоп. Полное поздравление', callback_data=cb.new(option='Текст_др', action='hi'))]
        keyboard_pust.add(*buttons_pust)
        await call.message.answer('\nПродолжим?', reply_markup=keyboard_pust)

    elif callback_data['option'] == 'Текст_др':
        await call.message.answer(str(sdr)+ ' ' + str(gelau) + ' ' +str(bud) + ' ' +str(pust) + '\n')
        keyboard_tdr = InlineKeyboardMarkup()
        buttons_tdr = [InlineKeyboardButton(text='Нет. Давай начнем с начала\n', callback_data=cb.new(option='С начала', action='hi')),
                      InlineKeyboardButton(text='Да, всё супер!', callback_data=cb.new(option='Супер', action='hi'))]
        keyboard_tdr.add(*buttons_tdr)
        await call.message.answer('\nПонравилось поздравление?\n', reply_markup=keyboard_tdr)

    elif callback_data['option'] == 'Супер':
        await bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEIqstkQkjTTlLB4k0JCWnXp3Y-1GLDIAACeysAAsCeeEkMEM9ffqD3Mi8E')
        await call.message.answer('Замечательно! Рада, что смогла помочь! Хорошего дня и до новых встеч!\n')

    elif callback_data['option'] == 'С начала':
        await bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEIiZpkNQgw0dzqUMCXfRsLrfcAASzlxRIAAr4oAAKqYHlJgmFIgvohYosvBA')
        await call.message.answer('Фыр-фыр! Надеюсь, что у нас получится с еще одной попытки!\n' + str(info_text))

    elif callback_data['option'] == 'С НГ':       # С Новым годом
        await call.message.answer(hb_sng_text())
        keyboard_sng = InlineKeyboardMarkup()
        buttons_sng = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='С НГ', action='hi')),
                      InlineKeyboardButton(text='Дальше\n', callback_data=cb.new(option='Некст_нг', action='hi')),
                      InlineKeyboardButton(text='Стоп.\nПолное поздравление\n', callback_data=cb.new(option='Текст_нг', action='hi'))]
        keyboard_sng.add(*buttons_sng)
        await call.message.answer('\nПродолжим?', reply_markup=keyboard_sng)

    elif callback_data['option'] == 'Некст_нг':
        keyboard_nng = InlineKeyboardMarkup()
        buttons_nng = [InlineKeyboardButton(text='Я желаю ...\n', callback_data=cb.new(option='Я желаю', action='hi')),
                      InlineKeyboardButton(text='И пусть ...\n', callback_data=cb.new(option='И пусть', action='hi'))]
        keyboard_nng.add(*buttons_nng)
        await call.message.answer('Как продолжим поздравление?', reply_markup=keyboard_nng)

    elif callback_data['option'] == 'Я желаю':
        await call.message.answer(hb_yagelau_text())
        keyboard_yagelau = InlineKeyboardMarkup()
        buttons_yagelau = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='Я желаю', action='hi')),
                          InlineKeyboardButton(text='Дальше\n', callback_data=cb.new(option='И пусть', action='hi')),
                          InlineKeyboardButton(text='Стоп. Полное поздравление\n', callback_data=cb.new(option='Текст_нг', action='hi'))]
        keyboard_yagelau.add(*buttons_yagelau)
        await call.message.answer('\nПродолжим?', reply_markup=keyboard_yagelau)

    elif callback_data['option'] == 'И пусть':
        await call.message.answer(hb_ipust_text())
        keyboard_ipust = InlineKeyboardMarkup()
        buttons_ipust = [InlineKeyboardButton(text='Другое\n', callback_data=cb.new(option='И пусть', action='hi')),
                        InlineKeyboardButton(text='Стоп. Полное поздравление\n', callback_data=cb.new(option='Текст_нг', action='hi'))]
        keyboard_ipust.add(*buttons_ipust)
        await call.message.answer('\nПродолжим?', reply_markup=keyboard_ipust)

    elif callback_data['option'] == 'Текст_нг':
        await call.message.answer(str(sng)+ ' ' + str(yagelau) + ' ' +str(ipust))
        keyboard_tng = InlineKeyboardMarkup()
        buttons_tng = [InlineKeyboardButton(text='Нет. Давай начнем с начала\n', callback_data=cb.new(option='С начала', action='hi')),
                      InlineKeyboardButton(text='Да, всё супер!', callback_data=cb.new(option='Супер', action='hi'))]
        keyboard_tng.add(*buttons_tng)
        await call.message.answer('\nПонравилось поздравление?\n', reply_markup=keyboard_tng)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)                  # Запускает проверку сообщений в диалоге (запускает бота)

  