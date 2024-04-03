import os
import torch
import queue
import numpy as np
import speech_recognition as sr
import pynput.keyboard
from faster_whisper import WhisperModel

keyboard = pynput.keyboard.Controller()

model_root = os.path.expanduser("~/.cache/whisper")
audio_model = WhisperModel("distil-small.en", download_root=model_root, device="auto", compute_type="int8")

audio_queue = queue.Queue()

recorder = sr.Recognizer()
recorder.energy_threshold = 300
recorder.dynamic_energy_threshold = False
hallucinate_threshold = 40

source = sr.Microphone(sample_rate=16000)
with source: recorder.adjust_for_ambient_noise(source)

def record_queue_pop():
    audio = b"".join([audio_queue.get() for _ in range(audio_queue.qsize())])
    return sr.AudioData(audio,16000,2).get_raw_data()

def record_queue_push(_, audio):
    audio_queue.put_nowait(audio.get_raw_data())
recorder.pause_threshold = 5
recorder.listen_in_background(source, record_queue_push, phrase_time_limit=5)


while True:
    audio_frame = np.frombuffer(record_queue_pop(), dtype=np.int16)

    loudness = np.sqrt(np.mean(np.square(audio_frame)))
    if loudness < hallucinate_threshold:
        continue

    to_write = ''
    audio_data = audio_frame.flatten().astype(np.float32) / 32768.0
    segments, _ = audio_model.transcribe(audio_data)
    to_write = ''.join([segment.text for segment in segments])

    if to_write: keyboard.type(to_write) # [" ","\n"]: