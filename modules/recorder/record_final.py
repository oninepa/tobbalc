# record_final.py - 화면 + 음성 + 키보드 로그
import mss
import cv2
import numpy as np
import pyaudio
import threading
import json
import time
from datetime import datetime
from pynput import keyboard, mouse

# 설정
WIDTH, HEIGHT = 1920, 1080
FPS = 10
RECORD_TIME = 60  # 테스트용 60초
OUTPUT_VIDEO = f"recordings/human/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
OUTPUT_AUDIO = f"recordings/human/voice_raw.wav"
OUTPUT_LOG = f"recordings/human/input_log.json"

# 폴더 생성
import os
os.makedirs("recordings/human", exist_ok=True)

# 화면 녹화
def record_screen():
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (WIDTH, HEIGHT))

    start_time = time.time()
    while time.time() - start_time < RECORD_TIME:
        img = np.array(sct.grab(monitor))
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        out.write(img_bgr)
        if cv2.waitKey(1) == 27:  # ESC
            break
    out.release()
    print("화면 녹화 완료")

# 음성 녹화
def record_audio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    print("음성 녹화 시작...")
    for _ in range(0, int(RATE / CHUNK * RECORD_TIME)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    import wave
    wf = wave.open(OUTPUT_AUDIO, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("음성 녹화 완료")

# 키보드 로그
key_log = []
def on_press(key):
    try:
        key_log.append({"time": time.time(), "event": "press", "key": key.char})
    except AttributeError:
        key_log.append({"time": time.time(), "event": "press", "key": str(key)})

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def record_keyboard():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# 마우스 로그 (옵션)
mouse_log = []
def on_click(x, y, button, pressed):
    if pressed:
        mouse_log.append({"time": time.time(), "event": "click", "x": x, "y": y, "button": str(button)})

def record_mouse():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

# 종료 후 저장
def save_logs():
    time.sleep(1)
    with open(OUTPUT_LOG, "w", encoding="utf-8") as f:
        json.dump({"keyboard": key_log, "mouse": mouse_log}, f, indent=2, ensure_ascii=False)
    print("입력 로그 저장 완료")

if __name__ == "__main__":
    print("녹화 시작 준비 중...")
    time.sleep(2)

    # 병렬 실행
    t1 = threading.Thread(target=record_screen)
    t2 = threading.Thread(target=record_audio)
    t3 = threading.Thread(target=record_keyboard)
    t4 = threading.Thread(target=record_mouse)

    t1.start(); t2.start(); t3.start(); t4.start()
    t1.join(); t2.join(); t3.join(); t4.join()

    save_logs()
    print("모든 녹화 완료:", OUTPUT_VIDEO)# record_final.py - 화면 + 음성 + 키보드 로그
import mss
import cv2
import numpy as np
import pyaudio
import threading
import json
import time
from datetime import datetime
from pynput import keyboard, mouse

# 설정
WIDTH, HEIGHT = 1920, 1080
FPS = 10
RECORD_TIME = 60  # 테스트용 60초
OUTPUT_VIDEO = f"recordings/human/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
OUTPUT_AUDIO = f"recordings/human/voice_raw.wav"
OUTPUT_LOG = f"recordings/human/input_log.json"

# 폴더 생성
import os
os.makedirs("recordings/human", exist_ok=True)

# 화면 녹화
def record_screen():
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (WIDTH, HEIGHT))

    start_time = time.time()
    while time.time() - start_time < RECORD_TIME:
        img = np.array(sct.grab(monitor))
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        out.write(img_bgr)
        if cv2.waitKey(1) == 27:  # ESC
            break
    out.release()
    print("화면 녹화 완료")

# 음성 녹화
def record_audio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    print("음성 녹화 시작...")
    for _ in range(0, int(RATE / CHUNK * RECORD_TIME)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    import wave
    wf = wave.open(OUTPUT_AUDIO, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("음성 녹화 완료")

# 키보드 로그
key_log = []
def on_press(key):
    try:
        key_log.append({"time": time.time(), "event": "press", "key": key.char})
    except AttributeError:
        key_log.append({"time": time.time(), "event": "press", "key": str(key)})

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def record_keyboard():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# 마우스 로그 (옵션)
mouse_log = []
def on_click(x, y, button, pressed):
    if pressed:
        mouse_log.append({"time": time.time(), "event": "click", "x": x, "y": y, "button": str(button)})

def record_mouse():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

# 종료 후 저장
def save_logs():
    time.sleep(1)
    with open(OUTPUT_LOG, "w", encoding="utf-8") as f:
        json.dump({"keyboard": key_log, "mouse": mouse_log}, f, indent=2, ensure_ascii=False)
    print("입력 로그 저장 완료")

if __name__ == "__main__":
    print("녹화 시작 준비 중...")
    time.sleep(2)

    # 병렬 실행
    t1 = threading.Thread(target=record_screen)
    t2 = threading.Thread(target=record_audio)
    t3 = threading.Thread(target=record_keyboard)
    t4 = threading.Thread(target=record_mouse)

    t1.start(); t2.start(); t3.start(); t4.start()
    t1.join(); t2.join(); t3.join(); t4.join()

    save_logs()
    print("모든 녹화 완료:", OUTPUT_VIDEO)