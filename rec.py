import json
import time

from typing import Iterator, Callable

import pyaudio
import vosk


class Recognize:
    def __init__(self):
        model = vosk.Model('vosk-model-small-ru-0.22')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                              channels=1,
                              rate=16000,
                              input=True,
                              frames_per_buffer=8000)

    def listen(self) -> Iterator[str]:
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']

    def start(self) -> None:
        self.stream.start_stream()

    def pause(self) -> None:
        self.stream.stop_stream()

    def safe_speak(self, text: str, f: Callable[[str], None]) -> None:
        self.pause()
        f(text)
        time.sleep(0.5)
        self.start()
