import requests

openai_api_key = "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"


def query_chatgpt(query):
    # URL HTTP-интерфейса ChatGPT
    # query = 'Напиши еще крутой prompt для генерации изображений нейронной сетью ChatGPT, не повторяя предыдущие, - то о чем ты мечтаешь?'

    url = "https://api.openai.com/v1/chat/completions"

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

    #     # Вывод ответа на экран
    #     print("Ответ от ChatGPT:")
    #     print(answer)
    # else:
    #     print("Ошибка при выполнении запроса к ChatGPT: " + response.text)

    return answer


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
            # print(url)
            # image_data = requests.get(url).content
            # img = Image.open(io.BytesIO(image_data))
            # img.show()
            return url
    else:
        return 'Не удалось сгенерировать изображение.'
