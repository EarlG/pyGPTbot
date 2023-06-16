import os
import speech_recognition as sr
import pyttsx3
import openai

# Установите ключ API ChatGPT и настройки голосового движка pyttsx3
openai.api_key = os.environ['OPENAI_KEY']
# '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'
engine = pyttsx3.init()
# chatgpt_model = 'text-davinci-003'
chatgpt_model = 'gpt-3.5-turbo-0301'

# Задайте ключевое слово для активации помощника и ключевую фразу для завершения работы
KEYWORD = "гена"
STOP_KEYWORD = "стоп"


def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = r.listen(source)

    try:
        recognized_text = r.recognize_google(audio, language="ru-RU")
        print("Распознанный текст:", recognized_text)
        return recognized_text.lower()
    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи: {e}")

    return ""


def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()


def process_request(request):
    response = openai.Completion.create(
        engine=chatgpt_model,
        prompt=request,
        max_tokens=4000,
        temperature=0.7
    )
    return response.choices[0].text.strip()


def main():
    while True:
        # Слушаем речь
        recognized_text = speech_to_text()

        # Если ключевое слово найдено в начале фразы
        if recognized_text.startswith(KEYWORD):
            # Извлекаем запрос из фразы
            request = recognized_text[len(KEYWORD):].strip()

            # Если запрос не пустой, обрабатываем его
            if request:
                print("Выполняю запрос:", request)

                # Запрос к сервису ChatGPT
                response = process_request(request)

                # Озвучиваем ответ
                print("Ответ:", response)
                text_to_speech(response)
            else:
                print("Запрос пустой.")
        elif recognized_text == f"{STOP_KEYWORD} {KEYWORD}":
            print("Программа завершена.")
            break


if __name__ == "__main__":
    main()