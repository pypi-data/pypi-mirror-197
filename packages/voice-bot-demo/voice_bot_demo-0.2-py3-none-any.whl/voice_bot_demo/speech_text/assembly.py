import asyncio
import base64
import json
import os
import re

import pyaudio
import websockets

from voice_bot_demo.console import console
from voice_bot_demo.speech_text.interface import SpeechTextInterface

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


class AssemblySpeechText(SpeechTextInterface):
    def __init__(self, device_index, process_sentence) -> None:
        self._stream = self._open_stream(device_index=device_index)
        self._process_sentence = process_sentence
        self._url = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
        self._secret = os.environ.get("ASSEMBLYAI_API_SECRET")
        if not self._secret:
            console.print(
                "Error: ASSEMBLYAI_API_SECRET environment variable not set. Please set it to your AssemblyAI API secret and try again.",
                style="bold red",
            )
            exit(1)

    def _open_stream(self, device_index):
        p = pyaudio.PyAudio()
        return p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            input_device_index=device_index,
        )

    def _is_full_sentence(self, text):
        return bool(re.search(r"[.!?]\s*$", text))

    async def run(self) -> None:
        async with websockets.connect(
            self._url,
            extra_headers=(("Authorization", self._secret),),
            ping_interval=5,
            ping_timeout=20,
        ) as _ws:

            async def send():
                while True:
                    try:
                        data = self._stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data": str(data)})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedError:
                        break
                    except Exception as e:
                        raise e
                    await asyncio.sleep(0.01)

            async def receive():
                while True:
                    try:
                        result_str = await _ws.recv()
                        sentence = json.loads(result_str)["text"]
                        if self._is_full_sentence(sentence):
                            self._process_sentence(sentence)
                        elif sentence:
                            console.print(
                                f"Partial sentence: {sentence}", style="bold yellow"
                            )
                    except websockets.exceptions.ConnectionClosedError:
                        break
                    except Exception:
                        pass

            _send_result, _receive_result = await asyncio.gather(send(), receive())
