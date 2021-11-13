import telebot
import configury
from telebot import types
import sqlite3
import time
from SimpleQIWI import *
from telebot.apihelper import ApiTelegramException


client = telebot.TeleBot(configury.config['token'])


db = sqlite3.connect('allusbase.db', check_same_thread = False)
sql = db.cursor()

token = "1d5599af4184a39fdf5fc3c47c7fdf74"
phone = "+79063626918"
api = QApi(token=token, phone=phone)
print(api.balance)


queue = []
admins = [984674439]
global all_deps
all_deps = 0.0
global all_vivods
all_vivods = 0.0


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

def mining(message):
    name = message.from_user.first_name
    user_id = message.from_user.id
    for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = {user_id}"):
        ku = i[0]
        pribyl = ku/100*5
    for a in sql.execute(f"SELECT cash FROM users WHERE id = {user_id}"):
        balance = a[0]

    if not user_id in queue:
        sql.execute(f"UPDATE users SET cash = {pribyl + balance} WHERE id = {user_id}")
        db.commit()
        client.send_message(message.chat.id, f'*Вы успешно собрали* {pribyl}₽', parse_mode = "Markdown")
        queue.append(user_id)
        time.sleep(86400)
        queue.remove(user_id)
    else:
        client.send_message(message.chat.id, 'Вы сегодня уже собирали прибыль!')


#def invest_money(message):
    #msg = client.send_message(message.chat.id, 'Напишите сумму для инвестирования:')
    #client.register_next_step_handler(msg, investrub)
def investy(message):
    if message.text == '-':
        client.send_message(message.chat.id, 'Отмена действия')
    else:
        try:
            price = int(message.text)
            token = "1d5599af4184a39fdf5fc3c47c7fdf74"
            phone = "+79063626918"
            user_id = message.from_user.id
            api = QApi(token=token, phone=phone)
            db = sqlite3.connect('allusbase.db', check_same_thread = False)
            sql = db.cursor()
            comment = api.bill(price, comment = user_id)
            client.send_message(message.chat.id, f'*Для инвестирования переведите {price} руб.*\n*На QIWI:* {phone}\n*При оплате обязательно укажите комментарий: *{comment}')

            api.start()


            while True:
                token = "1d5599af4184a39fdf5fc3c47c7fdf74"
                phone = "+79063626918"
                api = QApi(token=token, phone=phone)
                db = sqlite3.connect('allusbase.db', check_same_thread = False)
                sql = db.cursor()
                comment = api.bill(price)

                if api.check(comment):
                    user_id = call.message.from_user.id
                    for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = {user_id}"):
                        balance = i[0]
                        break
                        sql.execute(f"UPDATE users SET cash_energy = {price + balance} WHERE id = {user_id}")
                        db.commit()
                        client.edit_message_text(chat_id = message.chat.id, message_id = message.message_id, text =  f'*✅Вы успешно инвестировали {price} руб!*')
                        all_deps += price
                        username = message.from_user.username
                        if username is None:
                            client.send_message(-1001638482952, f'Пользователь пополнил {price}₽\nПлатёжная система: QIWI', parse_mode = "Markdown")
                        else:
                            client.send_message(-1001638482952, f'[Пользователь](https://t.me/{username}) пополнил {price}₽*\nПлатёжная система: QIWI', parse_mode = "Markdown")

                        break


        except:
             client.send_message(message.chat.id, 'Введите корректное число!')



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
                client.send_message(rows[row][0], f'{message.text}')
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
        pricev = message.text
        user_id = message.from_user.id
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        for i in sql.execute(f"SELECT cash FROM users WHERE id = {user_id}"):
            balance = i[0]
            break
        if balance >= 1:
            sql.execute(f"UPDATE users SET cash = {balance - balance} WHERE id = {user_id}")
            db.commit()
            user_id = message.chat.id
            commisia = balance - balance/100*3
            client.send_message(user_id, '*✅Ваша заявка на вывод успешно создана и будет обработана в течении 24 часов!*', parse_mode = "Markdown")
            markup_inline = types.InlineKeyboardMarkup()
            item_pay = types.InlineKeyboardButton(text = 'Оплатить заявку', callback_data = 'pay')
            markup_inline.add(item_pay)
            client.send_message(-1001491637866, f'Заявка на вывод средств:\nID: {user_id}\nQIWI: {pricev}\nСумма вывода: {commisia}', reply_markup = markup_inline)
            @client.callback_query_handler(func=lambda call: True)
            def callcheckerpay(call):
                if call.data == 'pay':
                    client.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '✅Заявка оплачена')
                    token = "1d5599af4184a39fdf5fc3c47c7fdf74"
                    phone = "+79063626918"
                    api = QApi(token=token, phone=phone)
                    commisia = balance - balance/100*3
                    api.pay(account = f"{pricev}", amount = commisia)
                    client.send_message(user_id, f'*✅Ваша заявка на вывод средств одобрена!*\n💸На ваш QIWI зачислено *{commisia}₽*\n\nЕсли не сложно, оставьте свой отзыв командой /otzyv', parse_mode = "Markdown")
                    username = message.from_user.username
                    all_vivods += commisia
                    if username is None:
                        client.send_message(-1001638482952, f'Пользователь вывел {commisia}₽\nПлатёжная система: QIWI', parse_mode = "Markdown")
                    else:
                        client.send_message(-1001638482952, f'[Пользователь](https://t.me/{username}) вывел {commisia}₽*\nПлатёжная система: QIWI', parse_mode = "Markdown")

        else:
            client.send_message(message.chat.id, 'Недостаточно средств! Мин. сумма 1 руб.')

def otzovikto(message):
    text = message.text
    if message.text:
        markup_inline = types.InlineKeyboardMarkup(row_width = 1)
        item_otz = types.InlineKeyboardButton(text = 'Опубликовать', callback_data = 'rightotz')
        item_otzbad = types.InlineKeyboardButton(text = 'Отклонить', callback_data = 'badotz')
        markup_inline.add(item_otz, item_otzbad)
        client.send_message(-1001491637866, f'{text}', reply_markup = markup_inline)
        @client.callback_query_handler(func=lambda call: True)
        def callcheckerotz(call):
            if call.data == 'rightotz':
                client.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '✅Отзыв опубликован!')
                client.send_message(-1001664113231, f'{text}')
            elif call.data == 'badotz':
                client.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Отзыв отклонён')


@client.message_handler(commands = ['otzyv'])
def otzovik(message):
    msg = client.send_message(message.chat.id, 'Напишите свой отзыв в формате: отзыв от (ваш никнейм):\nсам текст отзыва\nесли хотите написать отзыв со скрином, напишите нашему админу: @The_Brigis')
    client.register_next_step_handler(msg, otzovikto)


def registration(message):
    if message.text == 'пропуск':
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
            sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (name, user_id, 0, 0.00, 0, None))
            db.commit()
            client.send_message(message.chat.id, 'Отлично! Вы зарегистрированы!')
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
                        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (name, user_id, 0, 0.00, 0, referrer))
                        db.commit()
                        client.send_message(message.chat.id, 'Отлично! Вы зарегистрированы!')
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
    item_referals = types.KeyboardButton(text = '👥Рефералы')
    item_techhelp = types.KeyboardButton(text = '❓Задать вопрос')
    item_info = types.KeyboardButton(text = '📕О боте')

    markup_reply.add( item_profile, item_factory, item_bonus, item_referals, item_techhelp, item_info)
    client.send_message(message.chat.id, 'Меню:',
        reply_markup = markup_reply
    )




@client.message_handler(content_types = ['text'])
def get_text(message):
    if message.text.lower() == '/start':
        client.send_message(message.chat.id, 'Привет! Ты попал в бота по заработку! Инвестируй деньги и получай прибыль ежедневно!')
        client.send_message(message.chat.id, 'Напиши обучение, если раньше не имел дела с подобными проектами')

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
                client.send_message(message.chat.id, f'*Ваше имя:* {name}\n\n*ID:* {user_id}\n\n*Ваш баланс:* {i[0]}₽\n\n*💸Всего пополнено:* {ab[0]}₽\n🤑*Всего выведено:* {all_vivods}₽', reply_markup = markup_inline, parse_mode = "Markdown")
                break
            
        @client.callback_query_handler(func=lambda call: True)
        def callba(call):
            if call.data == 'invest':
                msg = client.send_message(call.message.chat.id, 'Введите сумму для инвестирования( - для отмены действия):')
                client.register_next_step_handler(msg, investy)
            elif call.data == 'vivesty':
                msg = client.send_message(call.message.chat.id, 'Чтобы вывести заработанные средства, напишите номер QIWI кошелька (пример: +79834519045/+34879603122)\nЧтобы отменить действие, напишите -')
                client.register_next_step_handler(msg, vivodmoney)
    if message.text == '💵Мой доход':
        factory(message)
    if message.text == '🎁Бонус':
        url = 'https://t.me/rubchat'
        markup_inline = types.InlineKeyboardMarkup()
        item_stats = types.InlineKeyboardButton(text = 'Наш чат', url = url)
        item_spam = types.InlineKeyboardButton(text = 'Наш канал', url = 'https://t.me/rubmoneychannel')
        markup_inline.add(item_stats, item_spam)
        client.send_message(message.chat.id, f'Подпишись на наш телеграм чат и канал с ежедневными промокодами и бонусами!', reply_markup = markup_inline)
    if message.text == '❓Задать вопрос':
        msg = client.send_message(message.chat.id, f'Напишите свой вопрос сюда и вам ответит администратор или - для отмены:')
        client.register_next_step_handler(msg, questions)
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
            client.send_message(message.chat.id, f'*Твой реферальный код:* {url}\n\nПривлекай людей по этому коду и получай 7% от пополнений каждого реферала!\n\n*Вы пригласили: {numr} человек*', parse_mode = "Markdown")
            break
    if message.text == 'Собрать 💸':
        mining(message)

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
        row = cursor.execute(f'SELECT id FROM users').fetchone()
        amount_user_all = 0
        while row is not None:
            amount_user_all += 1
            row = cursor.fetchone()
        client.send_message(message.chat.id, f'*Информация о проекте:*\n\n*Пользователей в боте: {amount_user_all}*\n\n*Резерв проекта: {api.balance[0]}₽*', reply_markup = markup_inlines, parse_mode = "Markdown")
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
        item_back = types.KeyboardButton(text = '🚫Назад')
        admin_buttons.add(item_stats, item_spam, item_back)
        client.send_message(message.chat.id, 'Админ-панель:', reply_markup = admin_buttons)


def factory(message):
    user_id = message.from_user.id
    db = sqlite3.connect('allusbase.db', check_same_thread = False)
    sql = db.cursor()
    for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = '{user_id}'"):
        ku = i[0]
        pribyl = ku/100*5
        button_reply = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
        item_takes = types.KeyboardButton(text = 'Собрать 💸')
        item_back = types.KeyboardButton(text = '🚫Назад')
        button_reply.add(item_takes, item_back)
        client.send_message(message.chat.id, f'*🤑Ваш доход:*', parse_mode = "Markdown", reply_markup = types.ReplyKeyboardRemove())
        client.send_message(message.chat.id, f'*💸Всего инвестировано:* {ku}₽\n\n*💸Доход в день:*{pribyl}₽', reply_markup = button_reply, parse_mode = "Markdown")


if __name__ == '__main__': # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
       client.polling(none_stop=True) # запуск бота
    except Exception as e:
       print(e) # или import traceback; traceback.print_exc() для печати полной инфы
       time.sleep(15)
