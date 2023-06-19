import telebot
import requests
from genpromt01 import query_chatgpt

bot_token = '6200473625:AAHQggdvC2pXpATubj8COR7ogmP_y5-GRBc'
bot = telebot.TeleBot(bot_token)

# Установите ключ API OpenAI
openai_api_key = "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"

# Словарь для хранения текущего режима диалога для каждого пользователя
dialog_mode = {}


# Функция для отправки сообщения ChatGPT и получения ответа
def send_message_to_chatgpt(message):
    return query_chatgpt(message)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    buttons = [telebot.types.KeyboardButton(text='погода'),
               telebot.types.KeyboardButton(text='рисунок'),
               telebot.types.KeyboardButton(text='чат')]
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
    bot.send_message(message.chat.id, 'Введите URL рисунка:')
    dialog_mode[message.chat.id] = 'picture'


# Обработчик кнопки "чат"
@bot.message_handler(func=lambda message: message.text.lower() == 'чат')
def chat(message):
    bot.send_message(message.chat.id, 'Начинаем чат-диалог. Введите сообщение:')
    dialog_mode[message.chat.id] = 'chat'


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.lower()

    if chat_id in dialog_mode:
        mode = dialog_mode[chat_id]
        if mode == 'weather':
            # Обработка сообщений пользователя в режиме "погода"
            # Ваш код здесь
            bot.send_message(chat_id, f"Вы выбрали режим 'погода'. Введенный город: {text}")
        elif mode == 'picture':
            # Обработка сообщений пользователя в режиме "рисунок"
            # Ваш код здесь
            bot.send_message(chat_id, f"Вы выбрали режим 'рисунок'. Введенный URL: {text}")
        elif mode == 'chat':
            # Обработка сообщений пользователя в режиме "чат"
            # Ваш код здесь
            # Обработка сообщений пользователя в режиме "чат"
            response = send_message_to_chatgpt(text)
            bot.send_message(chat_id, response)
            # bot.send_message(chat_id, f"Вы выбрали режим 'чат'. Введенное сообщение: {text}")
    else:
        bot.send_message(chat_id, 'Неверный выбор. Пожалуйста, выберите пункт меню.')


bot.polling()
