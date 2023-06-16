import requests
import telebot


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


# Основной код программы
if __name__ == "__main__":
    # URL изображения для загрузки
    image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-Wjgzyiv7NxReYAOb6GGhonED/user-nPXziU6p8Zu4Vh7AZOyVGGeI/img-HRfOgqkiNknUaSlcCJwyi4zK.png?st=2023-06-15T08%3A24%3A19Z&se=2023-06-15T10%3A24%3A19Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-06-14T21%3A23%3A15Z&ske=2023-06-15T21%3A23%3A15Z&sks=b&skv=2021-08-06&sig=LFL50mJAtaXr0nkJubuzZJEiok3dQ8CGiIdvIaR5JC0%3D"

    # Подпись к изображению с популярными тегами
    caption = "Мое замечательное фото! #photooftheday #instagood"

    # Токен вашего бота Telegram
    # bot_token = "YOUR_BOT_TOKEN"
    # bot_token = "5924675290:AAFOMc8gHCFSJWa9fsJonQRO-cCEGCa3Zt8"
    bot_token = '6200473625:AAHQggdvC2pXpATubj8COR7ogmP_y5-GRBc'

    # ID канала, в который будет отправлено изображение
    # channel_id = "@your_channel"
    channel_id = "-1001910709745"

    # Загрузка изображения в канал Telegram
    upload_photo_to_channel(image_url, caption, bot_token, channel_id)
