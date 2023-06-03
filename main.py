# import pip
# pip.main(['install', 'pytelegrambotapi'])
# pip.main(['install', 'openai'])
# from pyowm.utils import config
# from pyowm.utils import timestamps

from webserver import keep_alive
import os
import telebot
from pyowm import OWM
import openai
from aichat import openai_chat

openai.api_key = os.environ['OPENAI_KEY']
my_bot_secret = os.environ['TELE_TOKEN1']
my_owm_secret = os.environ['OWM_TOKEN']

owm = OWM(my_owm_secret)
mgr = owm.weather_manager()

bot = telebot.TeleBot(my_bot_secret)


@bot.message_handler(content_types=['text'])
def send_echo(message):
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
        try:
            # Search for current weather in London (Great Britain) and get details

            # place_msk = "Moscow"
            # observation_msk = mgr.weather_at_place( place_msk )

            # w_msk = observation_msk.weather
            # temp_msk = w_msk.temperature('celsius')["temp"]

            # answer += "\r\nIn " + place_msk + ": "
            # answer += str(temp_msk)
            # answer += "C " + w_msk.detailed_status

            # model = "text-davinci-002"
            # # model = "babbage"
            # # model = "ada"
            # respai = openai.Completion.create(
            #   engine=model,
            #   prompt=place,
            #   max_tokens=1024,
            #   temperature=0.5,
            #   top_p=1,
            #   frequency_penalty=0,
            #   presence_penalty=0
            # )
            # answer = respai['choices'][0]['text']
            answer = openai_chat(place)
            # answer = 'Мила привет 😁'

        except Exception:
            answer = 'Location is not defined. Write the name of the city...'

    # Задаем текст, который нужно отправить
    long_text = answer + " EOF"

    # здесь нужно указать ваш текст

    # Разбиваем текст на части по 4096 символов
    text_parts = [long_text[i:i + 4096] for i in range(0, len(long_text), 4096)]

    # Отправляем каждую часть текста по очереди
    for part in text_parts:
        bot.send_message(message.chat.id, part)


keep_alive()  # запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(none_stop=True)
