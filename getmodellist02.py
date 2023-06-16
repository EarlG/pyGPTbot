import requests


def list_available_models():
    # url = "https://api.openai.com/v1/engines"
    url = "https://api.openai.com/v1/models"

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        models = response.json()["data"]
        print("Доступные модели OpenAI:")
        for model in models:
            print(model["id"])
            response1 = requests.get(url + '/' + model["id"], headers=headers)
            print(response1.text)
    else:
        print("Не удалось получить список моделей.")


if __name__ == "__main__":
    list_available_models()
