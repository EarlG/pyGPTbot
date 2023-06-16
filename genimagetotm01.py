import requests
from PIL import Image
import io
from genpromt01 import query_chatgpt
from uploadimgtotm import upload_photo_to_channel

# Установите ключ API OpenAI
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


if __name__ == "__main__":
    # prompt_text = 'Break the composition of [супереалистичных пятимерных изображений] photography into key elements and write them separated by commas, without explanation. Make near 10 key elements'
    description = query_chatgpt(
        'Напиши еще самый необыкновенный и потрясающий prompt из 36 слов для генерации супереалистичных пятимерных изображений, не повторяя предыдущие')

    # description = query_chatgpt(prompt_text)
    img_url = generate_image(
        description + ' (Supreme realism, five dimensions, imaging technology, multi-perspective rendering, advanced lighting techniques, high-resolution graphics, digital manipulation, hyper-realistic details, creative vision, artistic expression)')
    # Токен вашего бота Telegram
    bot_token = '6200473625:AAHQggdvC2pXpATubj8COR7ogmP_y5-GRBc'
    # ID канала, в который будет отправлено изображение
    channel_id = "-1001910709745"
    upload_photo_to_channel(img_url, description, bot_token, channel_id)
