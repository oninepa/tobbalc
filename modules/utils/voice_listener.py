# voice_listener.py - 실시간 음성 인식 + input_mapper 연동
import speech_recognition as sr
import threading
import time
from modules.utils.input_mapper import trigger_action_by_voice  # 추가

def listen_continuously():
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 음성 인식 대기 중... (종료: Ctrl+C)")

    while getattr(listen_thread, "do_run", True):
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                print("듣는 중... (3초 이내 말하세요)")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            text = r.recognize_google(audio, language="ko-KR")
            print(f"✅ 인식됨: '{text}'")

            # 키워드 매핑
            if any(word in text for word in ["공격", "때려", "죽여", "빨리", "빠르게"]):
                print("🎮 액션: 공격 (조이스틱 A 버튼)")
                # 추후 조이스틱 제어 코드 연결

            elif any(word in text for word in ["슈퍼", "파워", "변신", "특별공격"]):
                print("⚡ 액션: 슈퍼 스킬 (조이스틱 Right Trigger)")
                # Right Trigger 제어 예정

            elif any(word in text for word in ["친구해", "친구", "친구버튼"]):
                print("🔵 액션: 친구 만들기 (조이스틱 Y 버튼)")
                # Y 버튼

            elif any(word in text for word in ["친구 끊어", "친구삭제", "다시 Y"]):
                print("🔴 액션: 친구 끊기 (조이스틱 Y 버튼)")
                # Y 버튼 더블 클릭 또는 조건 추가

            elif any(word in text for word in ["지도 크게", "지도 켜", "지도"]):
                print("🗺️ 액션: 지도 켜기 (조이스틱 B 버튼)")
                # B 버튼

            elif any(word in text for word in ["지도 작게", "지도 꺼"]):
                print("🗺️ 액션: 지도 끄기 (조이스틱 B 버튼)")
                # B 버튼

            elif any(word in text for word in ["무기 바꿔", "무기 교체", "무기"]):
                print("🔄 액션: 무기 교환 (조이스틱 X 버튼)")
                # X 버튼
        
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f"오류: {e}")

# 전역 변수로 스레드 제어
listen_thread = None

def start_listening():
    global listen_thread
    listen_thread = threading.Thread(target=listen_continuously, daemon=True)
    listen_thread.start()
    return listen_thread

if __name__ == "__main__":
    start_listening()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listen_thread.do_run = False
        print("\n🛑 음성 인식 종료")