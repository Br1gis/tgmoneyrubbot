import telebot
import configury
from telebot import types
import sqlite3
import time
from datetime import datetime, date, timedelta
from SimpleQIWI import *
from telebot.apihelper import ApiTelegramException
from random import randint
import traceback
import pyqiwi
import menuska
from menuska import buttons

from pyqiwip2p import QiwiP2P
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime


client = telebot.TeleBot(configury.config['token'])

QIWI_PRIV_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImZzenY5NC0wMCIsInVzZXJfaWQiOiI3OTA2MzYyNjkxOCIsInNlY3JldCI6ImZlZjRhMTM1MDhjNjQwMzM3NzkwYzI4NGQ4ZjNkMWJmYjI5MGNjMjYxNmRiODU2M2NlZGJjN2E2YjhhNmVmZGIifX0="

p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
now = datetime.now()

db = sqlite3.connect('allusbase.db', check_same_thread = False)
sql = db.cursor()


token = "487e928fde827febbe01257b466a7ff5"
phone = "+79063626918"
wallet = pyqiwi.Wallet(token=token, number=phone)
print(wallet.balance())

queue = []
admins = [984674439, 2049152651]
global all_deps
all_deps = 0.0
global all_vivods
all_vivods = 0.0


global gid

global gsum

global sborid

global sborsum




def endgive(message):
    if message.text == 'Инвест':
        for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = {giveid}"):
            balance = i[0]
            sql.execute(f"UPDATE users SET cash_energy = {int(givesum) + balance} WHERE id = {giveid}")
            db.commit()
            client.send_message(message.chat.id, '✅ Успешно!')
            client.send_message(int(giveid), f'*Администратор начислил вам {givesum}₽ на баланс для инвестиций!*', parse_mode = 'Markdown')
            break
    if message.text == 'Вывод':
        for i in sql.execute(f"SELECT cash FROM users WHERE id = {giveid}"):
            balance = i[0]
            sql.execute(f"UPDATE users SET cash = {int(givesum) + balance} WHERE id = {giveid}")
            db.commit()
            client.send_message(message.chat.id, '✅ Успешно!')
            client.send_message(int(giveid), f'*Администратор начислил вам {givesum}₽ на баланс для вывода!*', parse_mode = 'Markdown')
            break


def givesum(message):
    global givesum
    givesum = message.text
    msg = client.send_message(message.chat.id, 'На какой баланс зачисляем?')
    client.register_next_step_handler(msg, endgive)


def giveid(message):
    if message.text == '-':
        client.send_message(message.chat.id, 'Отмена действия')
    else:
        global giveid
        giveid = message.text
        msg = client.send_message(message.chat.id, 'Напишите сумму для выдачи:')
        client.register_next_step_handler(msg, givesum)



def endsbor(message):
    if message.text == 'Инвест':
        for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = {sborid}"):
            balance = i[0]
            sql.execute(f"UPDATE users SET cash_energy = {balance - int(sborsum)} WHERE id = {sborid}")
            db.commit()
            client.send_message(message.chat.id, '✅ Успешно!')
            client.send_message(int(sborid), f'*Администратор забрал у вас {int(givesum)}₽ с баланса для инвестиций!*', parse_mode = 'Markdown')
            break
    elif message.text == 'Вывод':
        for i in sql.execute(f"SELECT cash FROM users WHERE id = {sborid}"):
            balance = i[0]
            sql.execute(f"UPDATE users SET cash = {balance - int(sborsum)} WHERE id = {sborid}")
            db.commit()
            client.send_message(message.chat.id, '✅ Успешно!')
            client.send_message(int(sborid), f'*Администратор забрал у вас {int(sborsum)}₽ с баланса для вывода!*', parse_mode = 'Markdown')
            break


def sborsum(message):
    global sborsum
    sborsum = message.text
    msg = client.send_message(message.chat.id, 'На какой баланс зачисляем?')
    client.register_next_step_handler(msg, endsbor)


def sborid(message):
    if message.text == '-':
        client.send_message(message.chat.id, 'Отмена действия')
    else:
        global sborid
        sborid = message.text
        msg = client.send_message(message.chat.id, 'Напишите сумму для выдачи:')
        client.register_next_step_handler(msg, sborsum)



def admanswer(message):
    client.send_message(us_id, f'*✅На ваш вопрос ответил администратор!*\n\nОтвет: {message.text}', parse_mode = "Markdown")

def questions(message):
    global us_id
    user_name = message.from_user.first_name
    us_id = message.from_user.id
    if message.text == '-':
        client.send_message(message.chat.id, 'Отмена действия')
    else:
        client.send_message(message.chat.id, f'*✅Ваш вопрос отправлен на рассмотрение администратору!*', parse_mode = "Markdown")
        msg = client.send_message(984674439, f'Вопрос от {user_name}\nID: {us_id}\nТекст вопроса: {message.text}')
        client.register_next_step_handler(msg, admanswer)


#def invest_money(message):
    #msg = client.send_message(message.chat.id, 'Напишите сумму для инвестирования:')
    #client.register_next_step_handler(msg, investrub)
def investy(message):
    if message.text == '-':
        client.send_message(message.chat.id, 'Отмена действия')
    else:
        try:
            db = sqlite3.connect('allusbase.db', check_same_thread = False)
            sql = db.cursor()
            for bal in sql.execute(f'SELECT cash_energy FROM users WHERE id = {message.chat.id}'):
                global userbal
                userbal = bal[0]
                break
            global bill
            global lifetime
            price = float(message.text)
            lifetime = 30
            comment = str(message.from_user.id)

            bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
            link_oplata = bill.pay_url
            dep_inline = types.InlineKeyboardMarkup()
            url_dep = types.InlineKeyboardButton(text = 'Оплатить', url = f'{link_oplata}')
            dep_inline.add(url_dep)
            client.send_message(message.chat.id, f'*Cпособ пополнения: *🥝QIWI\n\nДля пополнения оплатите {price}₽ по ссылке ниже.\nСрок действия ссылки: 30 минут', reply_markup = dep_inline, parse_mode = "Markdown")
            oplata_time = datetime.now() #Получаем текущее время
            datetime_delta = oplata_time + timedelta(minutes=lifetime) #Получаем разницу между датами.
            while True:
                db = sqlite3.connect('allusbase.db', check_same_thread = False)
                sql = db.cursor()
                status = p2p.check(bill_id=bill.bill_id).status #Проверка статуса оплаты
                if status == 'PAID': #Проверка, на то - дошла ли оплата до бота. Вслучае положительного ответа, он выполняет данный if.
                    sql.execute(f'UPDATE users SET cash_energy = {userbal + price} WHERE id = {message.chat.id}')
                    db.commit()
                    client.send_message(message.chat.id, f'*✅ Вы успешно инвестировали {price}₽!*', parse_mode = "Markdown")
                    client.send_message(-1001638482952, f'*Пользователь* инвестировал {price}₽ через QIWI', parse_mode = "Markdown")
                    fr = open('moneyusers.txt', 'r')
                    alliki = fr.readlines()
                    if not message.chat.id in alliki:
                        f = open('moneyusers.txt', 'a')
                        f.write(str(message.chat.id) + '\n')
                        f.close()
                        time.sleep(0.1)

                        break
                        
                    else:
                        break
                elif datetime.now() > datetime_delta: #Делаем проверку, на время оплаты. То есть в случае неоплаты в течении 7-ми минут, цикл прекращается.
                    break #Завершение цикла
                    time.sleep(0.1)



        except:
            client.send_message(message.chat.id, 'Введите корректное число!')
            print(traceback.format_exc())



def rassylka(message):
    if message.text == 'отмена':
        client.send_message(message.chat.id, 'Отмена действия')
    else:
        c = sqlite3.connect("allusbase.db")
        cur = c.cursor()

        cur.execute('SELECT id FROM users')
        rows = cur.fetchall()
        for row in range(len(rows)):
            if rows[row][0] is None:
                continue
            else:
                time.sleep(1)
                client.send_message(rows[row][0], f'{message.text}', parse_mode = "Markdown")
                print(rows[row][0])
            '''try:
                time.sleep(1)
                #client.send_message(rows[row][0], str(message.text))
                print(rows[row][0])
            except:
                pass
        client.send_message(message.chat.id, '✅ Рассылка завершена!')
        print(rows)'''
        client.send_message(984674439, '✅ Рассылка завершена!')




def vivodmoney(message):
    if message.text == '-':
        client.send_message(message.chat.id, 'Отмена действия')
    else:
        global pricev
        global user_id
        pricev = message.text
        user_id = message.from_user.id
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        for i in sql.execute(f"SELECT cash FROM users WHERE id = {user_id}"):
            global balance
            balance = i[0]
            break
        if balance >= 2:
            sql.execute(f"UPDATE users SET cash = {balance - balance} WHERE id = {user_id}")
            db.commit()
            user_id = message.chat.id
            global commisia
            commisia = balance - balance/100*3
            client.send_message(user_id, '*✅Ваша заявка на вывод успешно создана и будет обработана в течении 24 часов!*', parse_mode = "Markdown")
            markup_inline = types.InlineKeyboardMarkup()
            item_pay = types.InlineKeyboardButton(text = 'Оплатить заявку', callback_data = 'pay')
            markup_inline.add(item_pay)
            client.send_message(-1001491637866, f'Заявка на вывод средств:\nID: {user_id}\nQIWI: {pricev}\nСумма вывода: {commisia}', reply_markup = markup_inline)
                

        else:
            client.send_message(message.chat.id, '⛔️ Недостаточно средств! Мин. сумма 2 руб.')

def otzovikto(message):
    text = message.text
    if message.text:
        markup_inline = types.InlineKeyboardMarkup(row_width = 1)
        item_otz = types.InlineKeyboardButton(text = 'Опубликовать', callback_data = 'rightotz')
        item_otzbad = types.InlineKeyboardButton(text = 'Отклонить', callback_data = 'badotz')
        markup_inline.add(item_otz, item_otzbad)
        client.send_message(-1001491637866, f'{text}', reply_markup = markup_inline)
            


@client.message_handler(commands = ['otzyv'])
def otzovik(message):
    msg = client.send_message(message.chat.id, 'Напишите свой отзыв в формате: отзыв от (ваш никнейм):\nсам текст отзыва\nесли хотите написать отзыв со скрином, напишите нашему админу: @The_Brigis')
    client.register_next_step_handler(msg, otzovikto)


def registration(message):
    try:
        if message.text == 'пропуск' or message.text == 'Пропуск':
            user_id = message.from_user.id
            referrer = None
            db = sqlite3.connect('allusbase.db')
            sql = db.cursor()
            name = message.from_user.first_name
            user_id = message.from_user.id
            sql.execute(f"SELECT name FROM users WHERE id = {user_id}")
            if sql.fetchone() is None:
                user_id = message.from_user.id
                name = message.from_user.first_name
                sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (name, user_id, 0, 0.00, 0, None, 0.0))
                db.commit()
                client.send_message(message.chat.id, 'Отлично! Вы зарегистрированы!')
                buttons(message)
            else:
                buttons(message)
                for value in sql.execute("SELECT * FROM users"):
                    print(value)
        else:
            user_id = message.from_user.id
            referrer = int(message.text)
            db = sqlite3.connect('allusbase.db')
            sql = db.cursor()
            name = message.from_user.first_name
            user_id = message.from_user.id
            sql.execute(f'SELECT ownref FROM users WHERE id = {user_id}')
            if sql.fetchone() is None:
                sql.execute(f"SELECT name FROM users WHERE id = {user_id}")
                if sql.fetchone() is None:
                    for refik in sql.execute(f'SELECT id FROM users WHERE id = {referrer}'):
                        if refik is None:
                            client.send_message(message.chat.id, 'Промокод не найден! Попробуйте ещё раз!')
                            time.sleep(1)
                            register(message)
                        else:
                        
                            user_id = message.from_user.id
                            name = message.from_user.first_name
                            sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (name, user_id, 0, 0.00, 0, referrer, 0.0))
                            db.commit()
                            client.send_message(message.chat.id, 'Отлично! Вы зарегистрированы!\n\n *Также вы получаете 0.10₽ на баланс для вывода!*', parse_mode = 'Markdown')
                            buttons(message)
                            for p in sql.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
                                sql.execute(f'UPDATE users SET cash = {0.1 + p[0]} WHERE id = {message.chat.id}')
                                db.commit()
                            for i in sql.execute(f"SELECT referals FROM users WHERE id = {referrer}"):
                                balance = i[0]
                                sql.execute(f"UPDATE users SET referals = {1 + balance} WHERE id = {referrer}")
                                db.commit()
                                client.send_message(referrer, f'*Пользователь присоединился к боту по вашему коду!*\n\n💸Вы получили 0.15₽ на баланс для вывода!', parse_mode = "Markdown")
                                for b in sql.execute(f"SELECT cash FROM users WHERE id = {referrer}"):
                                    balance = b[0]
                                    sql.execute(f"UPDATE users SET cash = {0.15 + balance} WHERE id = {referrer}")
                                    db.commit()
                                    break
                else:
                    buttons(message)
                    for value in sql.execute("SELECT * FROM users"):
                        print(value)
            else:
                buttons(message)
                for value in sql.execute("SELECT * FROM users"):
                    print(value)
    except:
        client.send_message(message.chat.id, 'Ошибка! Попробуйте ввести команду /поехали ещё раз!')


@client.message_handler(commands = ['поехали'])
def register(message):
    msg = client.send_message(message.chat.id, f'Если у вас есть промокод пригласившего, введите его и получите бонус!\nЕсли промокода нет, напишите: пропуск')
    client.register_next_step_handler(msg, registration)





@client.message_handler(commands = ['menu'])
def buttons(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item_profile = types.KeyboardButton(text = '👨🏻‍💻Мой профиль')
    item_factory = types.KeyboardButton(text = '💵Мой доход')
    item_bonus = types.KeyboardButton(text = '🎁Бонус')
    item_plays = types.KeyboardButton(text = '🎲Игры')
    item_referals = types.KeyboardButton(text = '👥Рефералы')
    item_info = types.KeyboardButton(text = '📕О боте')

    markup_reply.add( item_profile, item_factory, item_bonus, item_plays, item_referals, item_info)
    client.send_message(message.chat.id, 'Меню:',
        reply_markup = markup_reply
    )
    





@client.message_handler(content_types = ['text'])
def get_text(message):
    if message.text.lower() == '/start':
        client.send_message(message.chat.id, 'Привет! Ты попал в бота по заработку! Инвестируй деньги и получай прибыль ежедневно!')
        client.send_message(message.chat.id, 'Напиши обучение, если раньше не имел дела с подобными проектами.\nЕсли ты уже имеешь опыт в этой сфере, напиши /поехали ')

    if message.text.lower() == 'обучение':
        url = 'https://t.me/joinchat/hw6npukv1684YzUy'
        client.send_message(message.chat.id, f'Вот тебе ссылочка на обучение: {url}')
        client.send_message(message.chat.id, 'Как будешь готов, напиши /поехали')
    if message.text == '👨🏻‍💻Мой профиль':
        markup_inline = types.InlineKeyboardMarkup(row_width = 1)
        item_invest = types.InlineKeyboardButton(text = '📤 Пополнить', callback_data = 'invest')
        item_vivod = types.InlineKeyboardButton(text = '📥 Вывести', callback_data = 'vivesty')
        markup_inline.add(item_invest, item_vivod)
        user_id = message.from_user.id
        name = message.from_user.first_name
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        for i in sql.execute(f'SELECT cash FROM users WHERE id = {user_id}'):
            for ab in sql.execute(f'SELECT cash_energy FROM users WHERE id = {user_id}'):
                client.send_message(message.chat.id, f'*Ваше имя:* {name}\n\n*ID:* {user_id}\n\n*Ваш баланс:* {round(i[0], 2)}₽\n\n*💸Всего пополнено:* {ab[0]}₽\n🤑*Всего выведено:* {round(all_vivods, 2)}₽', reply_markup = markup_inline, parse_mode = "Markdown")
                break
            
    if message.text == '💵Мой доход':
        factory(message)
    if message.text == '🎁Бонус':
        url = 'https://t.me/rubchat'
        markup_inline = types.InlineKeyboardMarkup()
        item_stats = types.InlineKeyboardButton(text = 'Наш чат', url = url)
        item_spam = types.InlineKeyboardButton(text = 'Наш канал', url = 'https://t.me/rubmoneychannel')
        markup_inline.add(item_stats, item_spam)
        client.send_message(message.chat.id, f'Подпишись на наш телеграм чат и канал с ежедневными промокодами и бонусами!', reply_markup = markup_inline)
    #if message.text == '❓Задать вопрос':
        #msg = client.send_message(message.chat.id, f'Напишите свой вопрос сюда и вам ответит администратор или - для отмены:')
        #client.register_next_step_handler(msg, questions)
    if message.text == 'Хочу такого же бота!':
        client.send_message(message.chat.id, 'Если вы хотите купить себе такого же бота, пишите ему: @The_Brigis')
    if message.text == 'админка':
        adminpanel(message)
    if message.text == '👥Рефералы':
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        for ref in sql.execute(f"SELECT referals FROM users WHERE id = {message.from_user.id}"):
            numr = ref[0]
            url = f'{message.from_user.id}'
            client.send_message(message.chat.id, f'*Твой реферальный код:* {url}\n\nПривлекай людей по этому коду и получай 0.15₽ за каждого реферала!\n\n*Вы пригласили: {numr} человек*', parse_mode = "Markdown")
            break
    if message.text == 'Собрать 💸':
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        if not message.chat.id in queue:
            for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = {message.chat.id}"):
                ku = i[0]
                pribyl = round(ku/100*4, 3)
                for p in sql.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
                    sql.execute(f'UPDATE users SET cash = {pribyl + p[0]} WHERE id = {message.chat.id}')
                    db.commit()
                    client.send_message(message.chat.id, f'*Вы успешно собрали {pribyl}₽*', parse_mode = "Markdown")
                    queue.append(message.chat.id)
                    time.sleep(86400)
                    queue.remove(message.chat.id)
                
        else:
            client.send_message(message.chat.id, f'Вы сегодня уже получали прибыль!')
            
            
        
            
            
            

    if message.text == '🚫Назад':
        buttons(message)
    if message.text == '📕О боте':
        token = "1d5599af4184a39fdf5fc3c47c7fdf74"
        phone = "+79063626918"
        api = QApi(token=token, phone=phone)
        markup_inlines = types.InlineKeyboardMarkup(row_width = 1)
        item_owner = types.InlineKeyboardButton(text = 'Владелец', url = 'https://t.me/The_Brigis')
        item_userlogs = types.InlineKeyboardButton(text = 'Выплаты и пополнения', url = 'https://t.me/depsandvivods')
        item_otzyvi = types.InlineKeyboardButton(text = 'Отзывы', url = 'https://t.me/otzrubmoneybot')
        item_wantbot = types.InlineKeyboardButton(text = 'Хочу такого же бота!', url = 'https://t.me/The_Brigis')
        markup_inlines.add(item_owner, item_userlogs, item_otzyvi, item_wantbot)
        conn = sqlite3.connect("allusbase.db")
        cursor = conn.cursor()
        row = cursor.execute(f'SELECT id FROM users')
        amount_user_all = 0
        while row is not None:
            amount_user_all += 1
            row = cursor.fetchone()
        client.send_message(message.chat.id, '❕ Информация о проекте:\n\n❕ Пользователей в боте - ' + str(amount_user_all), reply_markup = markup_inlines)
        conn.close()
    if message.text == 'Статистика':
        conn = sqlite3.connect("allusbase.db")
        cursor = conn.cursor()
        row = cursor.execute(f'SELECT id FROM users').fetchone()
        amount_user_all = 0
        while row is not None:
            amount_user_all += 1
            row = cursor.fetchone()
        client.send_message(message.chat.id, '❕ Информация:\n\n❕ Пользователей в боте - ' + str(amount_user_all))
        conn.close()
    if message.text == 'Рассылка':
        msg = client.send_message(message.chat.id, 'Напишите текст для рассылки(отмена, если хотите отменить действие):')
        client.register_next_step_handler(msg, rassylka)
    if message.text == 'Выдать 💸':
        msg = client.send_message(message.chat.id, f'Напишите id пользователя:')
        client.register_next_step_handler(msg, giveid)
    if message.text == 'Забрать 💸':
        msg = client.send_message(message.chat.id, f'Напишите id пользователя:')
        client.register_next_step_handler(msg, sborid)
    if message.text == '🎲Игры':
        client.send_message(message.chat.id, 'Переходим в раздел: 🎲Игры...', reply_markup = types.ReplyKeyboardRemove())
        time.sleep(2)
        markup_plays = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item_luckybox = types.KeyboardButton(text = '💎Коробка удачи')
        item_back = types.KeyboardButton(text = '🚫Назад')
        markup_plays.add(item_luckybox, item_back)
        client.send_message(message.chat.id, 'Выбирайте любую игру из меню!', reply_markup = markup_plays)
    if message.text == '💎Коробка удачи':
        play_inline = types.InlineKeyboardMarkup()
        item_openbox = types.InlineKeyboardButton(text = 'Купить коробку', callback_data = 'paybox')
        play_inline.add(item_openbox)
        client.send_message(message.chat.id, f'*💎Коробка удачи*\n\n*Суть игры:* Вы покупаете коробку удачи, в которой вам может попасться разная сумма денег, но коробка может оказаться и пустой!\n*Цена коробки:* 5₽', reply_markup = play_inline, parse_mode = "Markdown")
            




def adminpanel(message):
    if not message.from_user.id in admins:
        client.send_message(message.chat.id, 'Ошибка! Вы не являетесь администратором!')
    else:
        markup_inline = types.InlineKeyboardMarkup()
        item_stats = types.InlineKeyboardButton(text = 'Статистика', callback_data = 'stats')
        item_spam = types.InlineKeyboardButton(text = 'Рассылка', callback_data = 'spam')
        markup_inline.add(item_stats, item_spam)
        client.send_message(message.chat.id, 'Вы успешно авторизовались, как администратор!', reply_markup = types.ReplyKeyboardRemove())
        admin_buttons = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
        item_stats = types.KeyboardButton(text = 'Статистика')
        item_spam = types.KeyboardButton(text = 'Рассылка')
        item_gaveadm = types.KeyboardButton(text = 'Выдать 💸')
        item_sboradm = types.KeyboardButton(text = 'Забрать 💸')
        item_back = types.KeyboardButton(text = '🚫Назад')
        admin_buttons.add(item_stats, item_spam, item_gaveadm, item_sboradm, item_back)
        client.send_message(message.chat.id, 'Админ-панель:', reply_markup = admin_buttons)


def factory(message):
    user_id = message.from_user.id
    db = sqlite3.connect('allusbase.db', check_same_thread = False)
    sql = db.cursor()
    for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = '{user_id}'"):
        ku = i[0]
        pribyl = ku/100*4
        button_reply = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
        item_take = types.KeyboardButton(text = 'Собрать 💸')
        item_back = types.KeyboardButton(text = '🚫Назад')
        button_reply.add(item_take, item_back)
        client.send_message(message.chat.id, f'*🤑Ваш доход:*', parse_mode = "Markdown", reply_markup = types.ReplyKeyboardRemove())
        client.send_message(message.chat.id, f'*💸Всего инвестировано: * {ku}₽\n\n*💸Доход в минуту: * {round(pribyl/24/60, 3)}₽\n\n*💸Доход в час: * {round(pribyl/24, 3)}₽\n\n*💸Доход в день: * {round(pribyl, 2)}₽', reply_markup = button_reply, parse_mode = "Markdown")
        break


@client.callback_query_handler(func=lambda call: True)
def callba(call):
    db = sqlite3.connect('allusbase.db', check_same_thread = False)
    sql = db.cursor()
    if call.data == 'invest':
        msg = client.send_message(call.message.chat.id, 'Введите сумму для инвестирования( - для отмены действия):')
        client.register_next_step_handler(msg, investy)
    if call.data == 'vivesty':
        msg = client.send_message(call.message.chat.id, 'Чтобы вывести заработанные средства, напишите номер QIWI кошелька (пример: 79834519045/34879603122)\nЧтобы отменить действие, напишите -')
        client.register_next_step_handler(msg, vivodmoney)
    if call.data == 'pay':
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        
        client.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '✅Заявка оплачена')
        token = "487e928fde827febbe01257b466a7ff5"
        phone = "79063626918"
        commisia = balance - balance/100*3
        client.send_message(user_id, f'*✅Ваша заявка на вывод средств одобрена!*\n💸На ваш QIWI зачислено *{round(commisia, 2)}₽*\n\nЕсли не сложно, оставьте свой отзыв командой /otzyv', parse_mode = "Markdown")
        username = call.message.from_user.username
        wallet = pyqiwi.Wallet(token=token, number=phone)
        payment = wallet.send(pid=99, recipient=f'{pricev}', amount=commisia, comment='Выплата от: RubMoneyBot 💸')
        for r in sql.execute(f'SELECT vivods FROM users WHERE id = {message.chat.id}'):
            balviv = r[0]
            sql.execute(f'UPDATE users SET cash = {balviv + commisia}')
            db.commit()

            client.send_message(-1001638482952, f'*Пользователь* вывел {round(commisia, 2)}₽\nПлатёжная система: QIWI', parse_mode = "Markdown")
            break
    if call.data == 'paybox':
        prize = randint(0, 10)
        for u in sql.execute(f'SELECT cash FROM users WHERE id = {call.message.chat.id}'):
            if u[0] > 5:
                sql.execute(f'UPDATE users SET cash = {u[0] - 5}')
                db.commit()
                sql.execute(f'UPDATE users SET cash = {prize + u[0]}')
                db.commit()
                client.send_message(call.message.chat.id, f'*💎 Вы открыли коробку, и там оказалось: {prize}₽*', parse_mode = "Markdown", reply_markup = types.ReplyKeyboardRemove())
                time.sleep(1)
                buttons(call.message)
                break
            if u[0] < 5:
                client.send_message(call.message.chat.id, '⛔️ У вас недостаточно средств для открытия коробки!')
    if call.data == 'rightotz':
        client.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '✅Отзыв опубликован!')
        client.send_message(-1001664113231, f'{call.message.text}')
    if call.data == 'badotz':
        client.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Отзыв отклонён')
                


if __name__ == '__main__': # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
       client.polling(none_stop=True) # запуск бота
    except Exception as e:
       print(e) # или import traceback; traceback.print_exc() для печати полной инфы
       time.sleep(15)
