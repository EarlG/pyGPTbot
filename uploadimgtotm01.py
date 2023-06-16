import requests


def upload_photo_to_group(url, caption, bot_token, group_id):
    # Загрузка изображения
    response = requests.get(url)
    if response.status_code == 200:
        photo = response.content
    else:
        print("Ошибка при загрузке изображения.")

    # Отправка изображения в группу Telegram
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendPhoto",
        files={
            "photo": photo
        },
        data={
            "chat_id": group_id,
            "caption": caption
        }
    )

    if response.status_code == 200:
        print("Изображение успешно загружено в группу Telegram!")
    else:
        print("Ошибка при загрузке изображения в группу Telegram.")


# Основной код программы
if __name__ == "__main__":
    # URL изображения для загрузки
    image_url = "https://example.com/image.jpg"

    # Подпись к изображению с популярными тегами
    caption = "Мое замечательное фото! #photooftheday #instagood"

    # Токен вашего бота Telegram
    bot_token = "YOUR_BOT_TOKEN"

    # ID группы, в которую будет отправлено изображение
    group_id = -123456789

    # Загрузка изображения в группу Telegram
    upload_photo_to_group(image_url, caption, bot_token, group_id)
