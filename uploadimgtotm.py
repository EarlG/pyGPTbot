import requests
import telebot


# URL изображения для загрузки
# image_url = "https://oaidalleapiprodscus.blob.core.windows.net/

# Подпись к изображению с популярными тегами
# caption = "Мое замечательное фото! #photooftheday #instagood"

# Токен вашего бота Telegram
# bot_token = '6200473625:AAHQggdvC2pXpATubj8COR7ogmP_y5-GRBc'

# ID канала, в который будет отправлено изображение
# channel_id = "-1001910709745"

# Загрузка изображения в канал Telegram
# upload_photo_to_channel(image_url, caption, bot_token, channel_id)


def upload_photo_to_channel(url, caption, bot_token, channel_id):
    # Создание экземпляра бота
    bot = telebot.TeleBot(bot_token)

    # Загрузка изображения
    response = requests.get(url)
    if response.status_code == 200:
        photo = response.content
    else:
        print("Ошибка при загрузке изображения.")

    # Отправка изображения в канал Telegram
    photo_message = bot.send_photo(channel_id, photo, caption=caption)

    if photo_message:
        print("Изображение успешно загружено в канал Telegram!")
    else:
        print("Ошибка при загрузке изображения в канал Telegram.")
