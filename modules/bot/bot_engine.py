# bot_engine.py - 자율 게임봇 엔진
import cv2
import mss
import time
import json
import threading
from pyautogui import press, keyDown, keyUp
import pyautogui

pyautogui.FAILSAFE = False  # 화면 끝에서 멈추지 않도록

# 설정
RULES_FILE = "rules/rules_final.json"
MONITOR = {"top": 0, "left": 0, "width": 1920, "height": 1080}
FPS = 5

class GameBot:
    def __init__(self):
        self.running = False
        self.rules = self.load_rules()
        self.current_action = "대기 중"

    def load_rules(self):
        try:
            with open(RULES_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("rules", [])
        except:
            print("❌ 규칙 파일 없음, 기본 행동 모드")
            return []

    def take_action(self):
        # 더미 행동 (실제 인식은 향후)
        for rule in self.rules:
            if rule["type"] == "item" and rule["item"] == "자석" and rule["action"] == "수집":
                self.current_action = "자석 수집 명령"
                press('c')  # 무기 교체 예시
                time.sleep(0.5)
                return

        self.current_action = "이동 중"
        # 간단한 이동 사이클
        for key in ['w', 'a', 's', 'd']:
            if not self.running:
                break
            keyDown(key)
            time.sleep(0.3)
            keyUp(key)
            time.sleep(0.1)

    def start(self):
        self.running = True
        print("🟢 봇 실행 시작")
        while self.running:
            self.take_action()
            time.sleep(0.5)

    def stop(self):
        self.running = False
        print("🛑 봇 중지됨")

# CLI로 실행 시
if __name__ == "__main__":
    bot = GameBot()
    bot.start()