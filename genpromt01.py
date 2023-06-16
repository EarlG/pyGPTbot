import requests

def query_chatgpt(query):
    # URL HTTP-интерфейса ChatGPT
    # query = 'Напиши еще крутой prompt для генерации изображений нейронной сетью ChatGPT, не повторяя предыдущие, - то о чем ты мечтаешь?'

    url = "https://api.openai.com/v1/chat/completions"
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
