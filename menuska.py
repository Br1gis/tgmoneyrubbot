import telebot
import configury
from telebot import types
import sqlite3
import time
from datetime import datetime, date, timedelta

client = telebot.TeleBot(configury.config['token'])

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