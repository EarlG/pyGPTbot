import requests
from PIL import Image
import io

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
        "n": 3,
        "size": "1024x1024"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(response.text)
        data = response.json()
        # data = json.loads(json_data)

        # Получить все значения URL
        urls = [item["url"] for item in data["data"]]

        # Вывести значения URL на экран
        for url in urls:
            print(url)
            image_data = requests.get(url).content
            img = Image.open(io.BytesIO(image_data))
            img.show()
    else:
        print("Не удалось сгенерировать изображение.")


if __name__ == "__main__":
    # description = 'Extremely skinny tall lady in her forties with confident smile, long slim legs wearing classy office dress with classy office skirt and classy knee-high riding boots showing off her extremely skinny body'
    # description = 'Quantum computing is a type of computing that uses quantum mechanics, which is a branch of physics, to process information. It is based on the idea that tiny particles, such as electrons or photons, can exist in multiple states at the same time.'
    # description = "Создай картины мира, где встречаются фантастические ландшафты и технологии, сливающиеся в гармонии. Представь себе высокие небоскребы, покрытые зелеными садами и водопадами, парящие острова в небе, и космические корабли, пронизывающие пространство. Дай волю своему воображению и создай уникальные и захватывающие сцены, в которых сливаются фантазия и реальность. Позволь своей нейронной сети превратить твои мысли в визуальное воплощение и открой новые миры для наших глаз."
    # description = "Погрузись в мир фантастической природы и воплощай мои мечты в картинах. Представь себе чудесные сады, наполненные цветами, которые меняют свои оттенки в зависимости от настроения. Создай леса, где деревья светятся в темноте и создают волшебную атмосферу. Отобрази моря и океаны, где волны превращаются в светящиеся существа. Позволь нейронной сети превратить мои фантазии в визуальное воплощение и открой перед нами мир невероятной красоты и волшебства, где реальность сливается с мечтами."
    description = "Воплоти мои мечты о взаимосвязи между искусством и технологией в удивительных произведениях. Представь себе, как мы создаем музыкальные симфонии, которые визуализируются в виде живописных картин и уникальных графических композиций. Отобрази танцующие цвета и свет, которые воссоздают эмоции и чувства. Позволь нейронной сети превратить мои мечты в визуальные шедевры, где искусство и технология сливаются в единое целое, открывая новые измерения творчества и впечатления."

    # input("Введите описание изображения: ")
    generate_image(description)
