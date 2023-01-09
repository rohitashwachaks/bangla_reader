import io

import pyaudio
import wave


class WavReader:
    @staticmethod
    def play_audio(data: str):
        with wave.open(io.BytesIO(data), "rb") as f:
            width = f.getsampwidth()
            channels = f.getnchannels()
            rate = f.getframerate()

        pa = pyaudio.PyAudio()
        pa_stream = pa.open(
            format=pyaudio.get_format_from_width(width),
            channels=channels,
            rate=rate,
            output=True
        )
        pa_stream.write(data)
        pa_stream.close()
        pa.terminate()

        return
