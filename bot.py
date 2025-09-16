from config import *
from create_db import DB_Manager
from telebot import TeleBot
import sqlite3
from telebot import types
import time
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


bot = TeleBot(TOKEN)

conn = sqlite3.connect("help.db", check_same_thread=False)
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я чат бот который поможет тебе если у тебя возникли вопросы. 
/help - нажми на эту команду и узнаешь больше обо мне
""")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, """Выбери нужную тебе категорию:
✨ /Frequently - Самые задаваемые вопросы
📞 /Contacs - Наши контакты
📍 /Geoposition - Наша геолокация
💡 /Question - Задать свой вопрос
""")


@bot.message_handler(commands=['Frequently'])
def frequently(message):
    cursor.execute("SELECT id, questions FROM question")
    questions = cursor.fetchall()

    if not questions:
        bot.send_message(message.chat.id, "Вопросов пока нет.")
        return

    keyboard = types.InlineKeyboardMarkup()
    for q in questions:
        keyboard.add(types.InlineKeyboardButton(q[1], callback_data=str(q[0])))
    bot.send_message(message.chat.id, "Если хочешь вернуться то нажми /help")
    bot.send_message(message.chat.id, "Выбери вопрос, который у тебя возник:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    question_id = int(call.data)
    cursor.execute("SELECT answers FROM question WHERE id=?", (question_id,))
    result = cursor.fetchone()

    if result:
        bot.send_message(call.message.chat.id, result[0])
    else:
        bot.send_message(call.message.chat.id, "Ответ не найден.")

    time.sleep(2)
    help(call.message)



@bot.message_handler(commands=['Contacs'])
def contacs(message):
    bot.send_message(message.chat.id, """ 📞 Наши контакты:
    Email - restourante@gmail.com
    Tel - 896755284""")
    time.sleep(2)
    help(message)


@bot.message_handler(commands=['Geoposition'])
def geoposition(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Сдесь наш адрес", url="https://maps.app.goo.gl/7doPBH9W1befydJKA")
    keyboard.add(button)
    bot.send_message(message.chat.id, "📍 Мы находимся здесь - ",reply_markup=keyboard)
    time.sleep(2)
    help(message)


@bot.message_handler(commands=['Question'])
def ask_question(message):
    bm = bot.send_message(message.chat.id, "Напишите ваш вопрос:")
    bot.register_next_step_handler(bm, process_question, message.from_user.id, message.from_user.first_name)

def process_question(message, user_id, user_name):
    user_questions = message.text.strip()
    
    cursor.execute(
        "INSERT INTO feedback (user, name, questions) VALUES (?, ?, ?)",
        (user_id, user_name, user_questions)
    )
    conn.commit()
    
    bot.send_message(message.chat.id, "Спасибо! Ваш вопрос сохранен, и мы скоро ответим на него.")
    time.sleep(2)
    help(message)




if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()
