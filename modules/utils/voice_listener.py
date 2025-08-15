# voice_listener.py - 실시간 음성 인식
import speech_recognition as sr
import threading

def listen_continuously():
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 음성 인식 대기 중...")

    while getattr(listen_thread, "do_run", True):
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                print("듣는 중...")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)

            text = r.recognize_google(audio, language="ko-KR")
            print(f"인식됨: {text}")

            # 키워드 매핑
            if "공격" in text or "때려" in text:
                print("🟢 액션: 스페이스바 (공격)")
            elif "친구" in text:
                print("🔵 액션: B 키 (친구)")
            elif "지도" in text:
                print("🟡 액션: M 키 (지도)")

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f"오류: {e}")

# 백그라운드 스레드
listen_thread = threading.Thread(target=listen_continuously)
listen_thread.start()

if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listen_thread.do_run = False
        print("음성 인식 종료")