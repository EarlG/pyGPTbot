# import pip
# pip.main(['install', 'pytelegrambotapi'])
# pip.main(['install', 'openai'])
# from pyowm.utils import config
# from pyowm.utils import timestamps

from webserver import keep_alive
import os
import telebot
from telebot import types
from pyowm import OWM
import openai
from aichat import openai_chat
import time


def limit_function_calls(func, n_max=10, t_period=3600):
    count = 0
    last_call_time = 0

    def wrapper(*args, **kwargs):
        nonlocal count, last_call_time

        current_time = time.time()
        elapsed_time = current_time - last_call_time

        if count >= n_max and elapsed_time < t_period:
            print("Превышен лимит вызовов функции.")
        else:
            func(*args, **kwargs)
            count += 1
            last_call_time = current_time

    return wrapper


os.environ['OPENAI_KEY'] = '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'
os.environ['TELE_TOKEN1'] = '6200473625:AAHQggdvC2pXpATubj8COR7ogmP_y5-GRBc'
os.environ['OWM_TOKEN'] = 'f70b2868746d0a1f0c27740e7031549a'

openai.api_key = os.environ['OPENAI_KEY']
my_bot_secret = os.environ['TELE_TOKEN1']
my_owm_secret = os.environ['OWM_TOKEN']

owm = OWM(my_owm_secret)
mgr = owm.weather_manager()

# Инициализация бота
bot = telebot.TeleBot(my_bot_secret)

bot_mode = 'погода'


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)  # Создаем меню с кнопками
    buttons = ['?', 'погода', 'рисунок', 'chat', 'budget']
    markup.add(*[types.KeyboardButton(button) for button in buttons])

    bot.reply_to(message, 'Привет! Выберите опцию:', reply_markup=markup)


# Обработчик нажатия на кнопку
@bot.message_handler(func=lambda message: True)
def handle_button_click(message):
    global bot_mode
    button_text = message.text.lower()
    bot_mode = button_text
    if button_text == '?':
        bot.reply_to(message, 'Вы выбрали знак вопроса.')
        return
    elif button_text == 'погода':
        bot_mode = 'погода'
        bot.reply_to(message, 'Вы выбрали опцию "погода".')
        return
    elif button_text == 'рисунок':
        bot.reply_to(message, 'Вы выбрали опцию "рисунок".')
        return
    elif button_text == 'chat':
        bot.reply_to(message, 'Вы выбрали опцию "chat".')
        return
    elif button_text == 'budget':
        bot.reply_to(message, 'Вы выбрали опцию "budget".')
        return 

    # @bot.message_handler(content_types=['text'])
    # def send_echo(message):
    #     global bot_mode
    if bot_mode == '?':
        bot.reply_to(message, 'Вы выбрали знак вопроса.')
    elif bot_mode == 'погода':
        place = message.text
        try:
            # Search for current weather in London (Great Britain) and get details
            observation = mgr.weather_at_place(place)
            w = observation.weather
            temp = w.temperature('celsius')["temp"]

            answer = "In " + place + ": "
            answer += str(temp)
            answer += "C " + w.detailed_status
        except Exception:
            answer = 'Location is not defined. Write the name of the city...'
    elif bot_mode == 'рисунок':
        bot.reply_to(message, 'Вы выбрали опцию "рисунок".')
    elif bot_mode == 'chat':
        prompt = message.text
        try:
            answer = openai_chat(prompt)
        except Exception:
            answer = 'Chat error...'
    elif bot_mode == 'budget':
        bot.reply_to(message, 'Вы выбрали опцию "budget".')

    # Задаем текст, который нужно отправить
    long_text = answer + "\nEOF"

    # здесь нужно указать ваш текст

    # Разбиваем текст на части по 4096 символов
    text_parts = [long_text[i:i + 4096] for i in range(0, len(long_text), 4096)]

    # Отправляем каждую часть текста по очереди
    for part in text_parts:
        bot.send_message(message.chat.id, part)


# запускаем flask-сервер в отдельном потоке.
keep_alive()

# Запуск бота
bot.polling(none_stop=True)
