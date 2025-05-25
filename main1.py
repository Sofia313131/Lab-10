from voice import speak
from ai import AI
from rec import Recognize

# В данной работе мною был реализован простейший ИИ-агент с голосовым управлением.
# Он основан на бесплатном API pollinations.ai.
# Бот может работать с API всех 10-и вариантов и отвечать на запросы пользователя,
# сформулированные естественным языком.
# Единственная точная команда - "закрыть", которая завершает работу бота.

# Класс для распознавания речи
rec = Recognize()
rec.safe_speak('Начинаю работу', speak)
# Класс для обработки запросов
ai = AI()

for text in rec.listen():
    if text == 'закрыть':
        speak('До встречи!')
        quit()
    else:
        print(f"Вы сказали: {text}")
        # Ответ бота
        response = ai.ask(text)
        if response is not None:
            # Воспроизвести ответ
            rec.safe_speak(response, speak)
            print(f"Ответ: {response}")
        else:
            print("Запрос проигнорирован")