# input_mapper.py - 음성, 조이스틱, 키보드 통합 매핑
import time
import threading
from pynput import keyboard
import pygame  # 조이스틱 지원을 위해

# 초기화
pygame.init()
pygame.joystick.init()

# 조이스틱 연결 확인
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"🎮 조이스틱 감지됨: {joystick.get_name()}")
else:
    print("⚠️ 조이스틱 없음 - 테스트 모드로 실행")

# 음성 명령 → 조이스틱 액션 매핑
VOICE_TO_ACTION = {
    "공격": "joystick_button_A",
    "때려": "joystick_button_A",
    "죽여": "joystick_button_A",
    "빨리": "joystick_button_A",
    "빠르게": "joystick_button_A",

    "슈퍼": "joystick_right_trigger",
    "파워": "joystick_right_trigger",
    "변신": "joystick_right_trigger",
    "특별공격": "joystick_right_trigger",

    "친구해": "joystick_button_Y",
    "친구": "joystick_button_Y",
    "친구버튼": "joystick_button_Y",

    "친구 끊어": "joystick_button_Y",
    "친구를 끊어": "joystick_button_Y",
    "친구삭제": "joystick_button_Y",
    "다시 Y": "joystick_button_Y",

    "지도": "joystick_button_B",
    "지도 크게": "joystick_button_B",
    "지도 켜": "joystick_button_B",
    "지도 작게": "joystick_button_B",
    "지도 꺼": "joystick_button_B",

    "무기 바꿔": "joystick_button_X",
    "무기 교체": "joystick_button_X",
    "무기": "joystick_button_X",
}

# 키보드 → 조이스틱 매핑 (보조)
KEYBOARD_TO_ACTION = {
    'space': "joystick_button_A",
    'e': "joystick_right_trigger",
    'b': "joystick_button_B",
    'c': "joystick_button_X",
    'w': "joystick_up",
    's': "joystick_down",
    'a': "joystick_left",
    'd': "joystick_right",
}

# 현재 상태
current_action = "대기 중"
action_log = []

def log_action(action):
    global current_action
    current_action = action
    timestamp = time.strftime("%H:%M:%S")
    entry = f"[{timestamp}] 액션 실행: {action}"
    action_log.append(entry)
    print(entry)

# 조이스틱 입력 시뮬레이션 (실제 입력은 게임에서 감지)
def press_button(button):
    # 실제 조이스틱 제어는 하드웨어에 달려 있음
    # 여기선 로그만 출력 (실제 연동은 pygame 이벤트로 처리)
    log_action(f"🎮 조이스틱 - {button} 눌림")

# 음성/키보드 입력으로 액션 발생
def trigger_action_by_voice(command):
    action = VOICE_TO_ACTION.get(command)
    if action:
        if action == "joystick_button_A":
            press_button("A 버튼")
        elif action == "joystick_right_trigger":
            press_button("Right Trigger")
        elif action == "joystick_button_Y":
            press_button("Y 버튼")
        elif action == "joystick_button_B":
            press_button("B 버튼")
        elif action == "joystick_button_X":
            press_button("X 버튼")

def trigger_action_by_keyboard(key):
    action = KEYBOARD_TO_ACTION.get(key)
    if action:
        if action == "joystick_button_A":
            press_button("A 버튼")
        elif action == "joystick_right_trigger":
            press_button("Right Trigger")
        elif action == "joystick_button_Y":
            press_button("Y 버튼")
        elif action == "joystick_button_B":
            press_button("B 버튼")
        elif action == "joystick_button_X":
            press_button("X 버튼")
        elif action == "joystick_up":
            press_button("위 (조이스틱)")
        elif action == "joystick_down":
            press_button("아래 (조이스틱)")
        elif action == "joystick_left":
            press_button("왼쪽 (조이스틱)")
        elif action == "joystick_right":
            press_button("오른쪽 (조이스틱)")

# 키보드 리스너
def start_keyboard_listener():
    def on_press(key):
        try:
            if hasattr(key, 'char') and key.char:
                trigger_action_by_keyboard(key.char.lower())
            else:
                key_name = {keyboard.Key.space: 'space', keyboard.Key.esc: 'esc'}.get(key)
                if key_name:
                    trigger_action_by_keyboard(key_name)
        except Exception as e:
            print("키보드 오류:", e)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# 메인 루프 (조이스틱 입력 감지)
def listen_joystick():
    global current_action
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 조이스틱 버튼 입력
            elif event.type == pygame.JOYBUTTONDOWN:
                btn = event.button
                if btn == 0:
                    press_button("A 버튼")
                elif btn == 1:
                    press_button("B 버튼")
                elif btn == 2:
                    press_button("X 버튼")
                elif btn == 3:
                    press_button("Y 버튼")

        # 조이스틱 축 입력 (방향)
        if joystick:
            axis_x = joystick.get_axis(0)  # 왼쪽 조이스틱 X축
            axis_y = joystick.get_axis(1)  # Y축

            if axis_x < -0.5:
                press_button("왼쪽 (조이스틱)")
            elif axis_x > 0.5:
                press_button("오른쪽 (조이스틱)")
            if axis_y < -0.5:
                press_button("위 (조이스틱)")
            elif axis_y > 0.5:
                press_button("아래 (조이스틱)")

        clock.tick(20)

# 백그라운드 시작
def start_input_mapper():
    print("🎮 입력 매핑 시작: 음성, 키보드, 조이스틱 통합")
    start_keyboard_listener()
    thread = threading.Thread(target=listen_joystick, daemon=True)
    thread.start()
    return thread

if __name__ == "__main__":
    thread = start_input_mapper()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 입력 매핑 종료")