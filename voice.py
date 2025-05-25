import os
import sys
from urllib.parse import quote

import requests

instructions = ("Repeat the value of the \"Text to speech\" field verbatim, do not add anything else, do not delete"
                " anything, do not change anything, just say the text. IMPORTANT: Always speak the text in its entirety.\n\nVoice:"
                " Russian, without any accents, warm, empathetic, and professional, reassuring the customer that their"
                " issue is understood and will be resolved.\n\nPunctuation: Well-structured with natural pauses,"
                " allowing for clarity and a steady, calming flow.\n\nDelivery: Russian, without any accents, calm"
                " and patient, with a supportive and understanding tone that reassures the listener.\n\nPhrasing:"
                " Clear and concise, using customer-friendly language that avoids jargon while maintaining"
                " professionalism.\n\nTone: Empathetic and solution-focused, emphasizing both understanding and"
                " proactive assistance.\n\nLanguage: Russian, without any accents.\n\nText to speech: {0}")



def play(path: str) -> None:
    # Воспроизведение звука
    if sys.platform == "win32":
        os.startfile(path)
    else:
        os.system("mpg123 " + path)


def speak(text: str) -> None:
    # Генерация голоса на основе модели openai-audio
    with requests.session() as session:
        response = session.get(
            f"https://text.pollinations.ai/{quote(instructions.format(text))}",
            params={
                "model": "openai-audio",
                "voice": "ballad",
            },
        )
        # Сохранение результата
        with open("output.wav", "wb") as f:
            f.write(response.content)
        # Воспроизведение
        play("output.wav")
