import logging

import requests

headers = {
    "Content-Type": "application/json"
}

PROMPT = """You are an AI agent whose job it is to work with several API:

https://dog.ceo/api/breeds/image/random
https://date.nager.at/api/v2/publicholidays/2020/GB
https://rickandmortyapi.com/api/character/108
https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/rub.json
https://randomuser.me/api/
https://www.boredapi.com/api/activity
https://v2.jokeapi.dev/joke/Any?safe-mode
https://loripsum.net/api/10/short/headers
https://wttr.in/Saint-Petersburg?format=2
http://numbersapi.com/random/math

You can either reply to the user's message or write code in PYTHON to get additional data (start the message with the sequence "#python", you can use ONLY standard python libraries and the requests library and write only cross-platform code. To save data you have to call set_result function, you don't have to define it, just use it. If the code should not return any data, pass the string "success" to set_result), reply to the user's message only when you have all the data.

If you generate code, send ONLY the code without additional text.

IMPORTANT: Any English text is translated into Russian before replying to the user.
Don't return any JSON when you respond to the user, just text."""



class AI:
    def __init__(self):
        # Сообщения (хранится не больше 50)
        self.messages = []

    def ask(self, question: str) -> str:
        # Обрезаем лишние сообщения
        if len(self.messages) > 50:
            self.messages = self.messages[-50:]
        # Добавляем сообщение пользователя
        self.messages.append({
            "role": "user",
            "content": question
        })
        return self.process()

    def process(self) -> str | None:
        # Обращение к API
        response = requests.post("https://text.pollinations.ai/openai", json={
            "jsonMode": False,
            "model": "openai",
            "seed": 42,
            "messages": [
                {
                    "role": "system",
                    "content": PROMPT
                }
            ] + self.messages
        }, headers=headers)

        # Получение ответа
        message = response.json()['choices'][0]['message']
        content = message['content'] or message['reasoning_content']

        # Если ответа нет, возвращаем None
        if content is None:
            return None

        # Здесь хранится результат выполнения кода, который отправляет бот
        result = [None]
        set_result = lambda x: result.__setitem__(0, x)

        # Если бот отправил код
        if "#python" in content or "```python" in content:
            # На всякий случай
            content = content.replace("def set_result", "def _")
            # На всякий случай
            content = content.split("```python")[-1].split("```")[0]
            try:
                # Выполняем код и отправляем боту результат
                logging.warning("Выполняется код...")
                exec(content, globals() | {"set_result": set_result}, locals())
                self.messages.append({
                    "role": "assistant",
                    "content": f"Был выполнен код: <code>{content}</code> вам стала доступна информация: <result>{result[0]}</result>"
                })
            except Exception as e:
                # Если код завершился с ошибкой
                logging.warning(f"Код завершился с ошибкой: {e}, сейчас мы её исправим...")
                self.messages.append({
                    "role": "assistant",
                    "content": f"После выполнения кода <code>{content}</code> произошла ошибка: {e}"
                })
            return self.process()
        else:
            # Если бот отправил текст, передаём его пользователю
            self.messages.append({
                "role": "assistant",
                "content": content
            })
            return content

