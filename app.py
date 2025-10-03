import telebot
import requests
from genchatgpt import query_chatgpt
from genchatgpt import generate_image
from getweather import get_weather
from webserver import keep_alive
from datetime import datetime
import os

from pyowm import OWM
import time
import io
from gtts import gTTS

bot_token = '6200473625:AAHQggdvC2pXpATubj8COR7ogmP_y5-GRBc'
bot = telebot.TeleBot(bot_token)


def bot_log(message):
    bot_log_id = "-997031056"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = message.from_user.id
    user_name = message.from_user.username
    text = message.text
    bot.send_message(bot_log_id, f"{current_time}\nUser ID: {user_id} - {user_name}\n{text}")

def bot_log_text(text):
    bot_log_id = "-997031056"
    bot.send_message(bot_log_id, text)

# Your user ID: 5031535279
# Current chat ID: -997031056

# Установите ключ API OpenAI
openai_api_key = "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"

# Словарь для хранения текущего режима диалога для каждого пользователя
dialog_mode = {}


# Функция для отправки сообщения ChatGPT и получения ответа
def send_message_to_chatgpt(message):
    return query_chatgpt(message)


def weather_handler(message):
    city = message.text
    # Здесь выполняется запрос к веб-сервису погоды
    # Получаем данные погоды
    weather_data = get_weather_data(city)
    bot.send_message(message.chat.id, f"Данные погоды для города {city}:\n{weather_data}")
    # Запрашиваем название другого города
    bot.send_message(message.chat.id, "Введите название другого города:")


def image_handler(message):
    url = message.text
    # Загружаем рисунок по URL и публикуем его в заданном канале
    image_url = upload_image_to_channel(url)
    # Отправляем ссылку на рисунок в чат
    bot.send_message(message.chat.id, f"Рисунок опубликован в канале: {image_url}")


# функция генерации аудио из текста
import io
import pydub
from gtts import gTTS
from telebot import types


def generate_audio(chat_id, text):
    try:
        tts = gTTS(text=text, lang='ru')
        with io.BytesIO() as f:  # use a memory stream
            tts.write_to_fp(f)
            # tts.save(f)
            f.seek(0)
            bot.send_audio(chat_id, f)
    except Exception as e:
        bot.send_message(chat_id, "Ошибка при генерации аудио")


def audio_handler(message):
    text = message.text
    generate_audio(message.chat.id, text)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    buttons = [telebot.types.KeyboardButton(text='погода'),
         #      telebot.types.KeyboardButton(text='рисунок'),
         #      telebot.types.KeyboardButton(text='чат'),
               telebot.types.KeyboardButton(text='аудио')]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Выберите пункт меню:', reply_markup=keyboard)


# Обработчик кнопки "погода"
@bot.message_handler(func=lambda message: message.text.lower() == 'погода')
def weather(message):
    bot.send_message(message.chat.id, 'Введите название города:')
    dialog_mode[message.chat.id] = 'weather'


# Обработчик кнопки "рисунок"
@bot.message_handler(func=lambda message: message.text.lower() == 'рисунок')
def picture(message):
    bot.send_message(message.chat.id, 'Чей рисунок вы хотели бы увидеть?')
    dialog_mode[message.chat.id] = 'picture'


# Обработчик кнопки "чат"
@bot.message_handler(func=lambda message: message.text.lower() == 'чат')
def chat(message):
    bot.send_message(message.chat.id, 'Начинаем чат-диалог. Введите сообщение:')
    dialog_mode[message.chat.id] = 'chat'


# Обработчик кнопки "аудио"
@bot.message_handler(func=lambda message: message.text.lower() == 'аудио')
def audio(message):
    bot.send_message(message.chat.id, 'Введите текст для преобразования в аудио:')
    dialog_mode[message.chat.id] = 'audio'


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot_log(message)  # логирование
    chat_id = message.chat.id
    text = message.text.lower()
    if chat_id in dialog_mode:
        mode = dialog_mode[chat_id]
        if mode == 'weather':
            # Обработка сообщений пользователя в режиме "погода"
            # Ваш код здесь
            bot.send_message(chat_id, f"Вы выбрали режим 'погода'. Введенный город: {text}")
            bot.send_message(chat_id, get_weather(text))
        elif mode == 'picture':
            # Обработка сообщений пользователя в режиме "рисунок"
            # Ваш код здесь
            prompt_text = 'Напиши еще самый необыкновенный и потрясающий prompt из 36 слов для' \
                          ' генерации супереалистичных многомерных изображений сна ' + text + ', не повторяя предыдущие'
            # bot.send_message(chat_id, prompt_text)
            image_description = query_chatgpt(prompt_text)
            image_prompt = 'Dream of ' + text + '. ' + image_description + \
                           ' (Supreme realism, five dimensions, ' \
                           'imaging technology, multi-perspective rendering, advanced lighting techniques, ' \
                           'high-resolution graphics, digital manipulation, hyper-realistic details, creative' \
                           ' vision, artistic expression)'
            img_url = generate_image(image_prompt)
            response = requests.get(img_url)
            if response.status_code == 200:
                photo = response.content
            else:
                bot.send_message(chat_id, "Ошибка при загрузке изображения.")

            # Отправка изображения в канал Telegram
            photo_message = bot.send_photo(chat_id, photo, caption=image_description)

            channel_id = "-1001910709745"
            photo_message = bot.send_photo(channel_id, photo, caption=image_description)
            bot_log_text(image_prompt)

        elif mode == 'chat':
            # Обработка сообщений пользователя в режиме "чат"
            # Ваш код здесь
            response = send_message_to_chatgpt(text)
            bot.send_message(chat_id, response)
        elif mode == 'audio':
            # Обработка сообщений пользователя в режиме "аудио"
            # Ваш код здесь
            # bot.send_message(chat_id, f"Вы выбрали режим 'аудио'")
            generate_audio(chat_id, text)
    else:
        bot.send_message(chat_id, 'Неверный выбор. Пожалуйста, выберите пункт меню.')


# запускаем flask-сервер в отдельном потоке.
keep_alive()

# Запуск бота
bot.polling(none_stop=True)
