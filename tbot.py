import telebot
import configury
from telebot import types
import sqlite3
import time
from SimpleQIWI import *


client = telebot.TeleBot(configury.config['token'])


db = sqlite3.connect('allusbase.db', check_same_thread = False)
sql = db.cursor()

token = "1d5599af4184a39fdf5fc3c47c7fdf74"
phone = "+79063626918"
api = QApi(token=token, phone=phone)


queue = []


sql.execute("""CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    id INT,
    cash_energy FLOAT,
    cash FLOAT
)""")

db.commit()

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
        client.send_message(message.chat.id, f'Вы успешно собрали {pribyl}')
        queue.append(user_id)
        time.sleep(86400)
        queue.remove(user_id)
    else:
        client.send_message(message.chat.id, 'Вы сегодня уже собирали прибыль!')


#def invest_money(message):
    #msg = client.send_message(message.chat.id, 'Напишите сумму для инвестирования:')
    #client.register_next_step_handler(msg, investrub)



@client.message_handler(commands = ['поехали'])
def register(message):
    db = sqlite3.connect('allusbase.db')
    sql = db.cursor()
    name = message.from_user.first_name
    user_id = message.from_user.id
    sql.execute(f"SELECT name FROM users WHERE id = {user_id}")
    if sql.fetchone() is None:
        user_id = message.from_user.id
        name = message.from_user.first_name
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (name, user_id, 0, 0.00))
        db.commit()
        client.send_message(message.chat.id, 'Отлично! Вы зарегистрированы!')
    else:
        buttons(message)
        for value in sql.execute("SELECT * FROM users"):
            print(value)




@client.message_handler(commands = ['menu'])
def buttons(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item_profile = types.KeyboardButton(text = 'Мой профиль')
    item_invest = types.KeyboardButton(text = 'Инвестирoвать деньги')
    item_factory = types.KeyboardButton(text = 'Мой доход')
    item_take = types.KeyboardButton(text = 'Собрать прибыль')
    item_vivod = types.KeyboardButton(text = 'Вывод средств')

    markup_reply.add(item_invest, item_profile, item_factory, item_take, item_vivod)
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
    if message.text == 'Мой профиль':
        user_id = message.from_user.id
        name = message.from_user.first_name
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        for i in sql.execute(f'SELECT cash FROM users WHERE id = {user_id}'):
            client.send_message(message.chat.id, f'Ваш никнейм: {name}\nВаш ID: {user_id}\nВаш баланс: {i[0]}₽')
            break
    if message.text == 'Инвестирoвать деньги':
        client.send_message(message.chat.id, 'Чтобы пополнить баланс, введите инвестировать (сумма для пополнения) без скобок')
    elif 'инвестировать' in message.text.lower():
        arg = message.text.split(maxsplit=1)[1]
        price = int(arg)
        token = "1d5599af4184a39fdf5fc3c47c7fdf74"
        phone = "+79063626918"
        user_id = message.from_user.id
        api = QApi(token=token, phone=phone)
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        comment = api.bill(price)
        client.send_message(message.chat.id, f'Для инвестирования переведите {price} руб.\nНа QIWI: {phone}\nПри оплате обязательно укажите комментарий {comment}')

        api.start()

        while True:
            if api.check(comment):
                user_id = message.from_user.id
                for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = {user_id}"):
                    balance = i[0]
                    break
                sql.execute(f"UPDATE users SET cash_energy = {price + balance} WHERE id = {user_id}")
                db.commit()
                client.send_message(message.chat.id, f'✅Вы успешно инвестировали {price}!')
                break
  # если "аргумент" цифра
    if message.text == 'Мой доход':
        factory(message)
    if message.text == 'Собрать прибыль':
        mining(message)
    if message.text == 'Вывод средств':
        client.send_message(message.chat.id, 'Чтобы вывести заработанные средства, напишите вывести (номер вашего QIWI кошелька без скобок)')
    if 'вывести' in message.text.lower():
        argv = message.text.split(maxsplit=12)[1]
        pricev = float(argv)
        user_id = message.from_user.id
        db = sqlite3.connect('allusbase.db', check_same_thread = False)
        sql = db.cursor()
        for i in sql.execute(f"SELECT cash FROM users WHERE id = {user_id}"):
            balance = i[0]
            break
        if balance >= 1:
            sql.execute(f"UPDATE users SET cash = {balance - balance} WHERE id = {user_id}")
            db.commit()
            client.send_message(message.chat.id, '✅Ваша заявка на вывод успешно создана и будет обработана в течении 24 часов!')
            client.send_message(-796101984, f'Заявка на вывод средств:\nID: {user_id}\nQIWI: {pricev}\nСумма вывода: {balance}')
        else:
            client.send_message(message.chat.id, 'Недостаточно средств! Мин. сумма 1 руб.')


def factory(message):
    user_id = message.from_user.id
    db = sqlite3.connect('allusbase.db', check_same_thread = False)
    sql = db.cursor()
    for i in sql.execute(f"SELECT cash_energy FROM users WHERE id = '{user_id}'"):
        ku = i[0]
        pribyl = ku/100*5
        client.send_message(message.chat.id, f'Ваша доходность\nПроизводительность завода: {pribyl}/день')


client.enable_save_next_step_handlers(delay = 2)
client.load_next_step_handlers()
client.polling(none_stop = True, interval = 0)
