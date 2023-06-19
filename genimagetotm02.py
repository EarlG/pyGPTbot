import requests
import telebot
from PIL import Image
import io

openai_api_key = "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"
def query_chatgpt(query):
    # URL HTTP-интерфейса ChatGPT
    # query = 'Напиши еще крутой prompt для генерации изображений нейронной сетью ChatGPT, не повторяя предыдущие, - то о чем ты мечтаешь?'

    url = "https://api.openai.com/v1/chat/completions"
    # openai_api_key = "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"
    openai_api_key = "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"

    # Заголовки запроса
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    # Тело запроса в формате JSON
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    }

    # Отправка POST-запроса к ChatGPT
    response = requests.post(url, headers=headers, json=data)
    answer = 'гладиолус'

    if response.status_code == 200:
        # Получение ответа от ChatGPT
        result = response.json()

        # Извлечение ответа пользователя
        answer = result['choices'][0]['message']['content']

        # Вывод ответа на экран
        print("Ответ от ChatGPT:")
        print(answer)
    else:
        print("Ошибка при выполнении запроса к ChatGPT: " + response.text)

    return answer


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


# Установите ключ API OpenAI
# openai_api_key = "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"
openai_api_key = "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"


def generate_image(description):
    url = "https://api.openai.com/v1/images/generations"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "prompt": f"Generate an image based on the following description: {description}",
        "n": 1,
        "size": "1024x1024"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # print(response.text)
        data = response.json()
        # data = json.loads(json_data)

        # Получить все значения URL
        urls = [item["url"] for item in data["data"]]

        # Вывести значения URL на экран
        for url in urls:
            print(url)
            # image_data = requests.get(url).content
            # img = Image.open(io.BytesIO(image_data))
            # img.show()
            return url
    else:
        print("Не удалось сгенерировать изображение.")
        return ''


def gen_img_to_tm():
    # prompt_text = 'Break the composition of [супереалистичных пятимерных изображений] photography into key elements and write them separated by commas, without explanation. Make near 10 key elements'
    description = query_chatgpt(
        'Напиши еще самый необыкновенный и потрясающий prompt из 36 слов для генерации реалистичных пятимерных изображений человека, не повторяя предыдущие')

    # description = query_chatgpt(prompt_text)
    img_url = generate_image(
        description + ',powerful hypnotic suggestion of eloquence, Supreme realism, five dimensions, imaging technology, multi-perspective rendering, advanced lighting techniques, high-resolution graphics, digital manipulation, hyper-realistic details, creative vision')
    # Токен вашего бота Telegram
    bot_token = '6200473625:AAHQggdvC2pXpATubj8COR7ogmP_y5-GRBc'
    # ID канала, в который будет отправлено изображение
    channel_id = "-1001910709745"
    upload_photo_to_channel(img_url, description, bot_token, channel_id)


if __name__ == "__main__":
    gen_img_to_tm()
