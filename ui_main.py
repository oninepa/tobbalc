# ui_main.py
import sys
import os
import subprocess
import threading
import json
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QLabel, QFileDialog, QTextEdit
)
from PySide6.QtCore import Qt

# 🤖 봇 엔진 임포트 (수정된 버전)
from bot.bot_engine import GameBot


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autobot - King of Clabs")
        self.setGeometry(100, 100, 600, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.buttons = [
            ("봇 실행", self.open_bot),
            ("녹화", self.open_record),
            ("전처리", self.open_preprocess),
            ("학습", self.open_learn),
            ("기타 설정", self.open_settings)
        ]

        for text, func in self.buttons:
            btn = QPushButton(text)
            btn.clicked.connect(func)
            layout.addWidget(btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_bot(self):
        self.bot_window = QWidget()
        self.bot_window.setWindowTitle("봇 실행")
        self.bot_window.setGeometry(300, 300, 500, 300)

        layout = QVBoxLayout()

        self.bot_status = QLabel("🟢 상태: 중지됨")
        self.bot_action = QLabel("🤖 최근 행동: 없음")

        btn_start = QPushButton("▶️ 봇 실행")
        btn_pause = QPushButton("⏸️ 일시중지")
        btn_stop = QPushButton("■ 완전 중지")
        btn_toggle = QPushButton("🔲 창크게")

        # 🤖 봇 인스턴스 생성
        self.bot = GameBot(status_callback=lambda msg: self.bot_action.setText(f"🤖 {msg}"))

        btn_start.clicked.connect(lambda: [
            self.bot_status.setText("🟢 상태: 실행 중"),
            self.bot.start()
        ])
        btn_pause.clicked.connect(lambda: self.bot_status.setText("🟡 상태: 일시중지"))
        btn_stop.clicked.connect(lambda: [
            self.bot_status.setText("🔴 상태: 중지됨"),
            self.bot.stop()
        ])

        self.terminal_shown = False
        def toggle_terminal():
            self.terminal_shown = not self.terminal_shown
            btn_toggle.setText("🔽 창작게" if self.terminal_shown else "🔲 창크게")
        btn_toggle.clicked.connect(toggle_terminal)

        layout.addWidget(self.bot_status)
        layout.addWidget(self.bot_action)
        layout.addWidget(btn_start)
        layout.addWidget(btn_pause)
        layout.addWidget(btn_stop)
        layout.addWidget(btn_toggle)
        self.bot_window.setLayout(layout)
        self.bot_window.show()

    def open_record(self):
        self.open_window("녹화")

    def open_window(self, title):
        self.sub_window = QWidget()
        self.sub_window.setWindowTitle(title)
        self.sub_window.setGeometry(300, 300, 500, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{title} 창 - 준비 중"))
        self.sub_window.setLayout(layout)
        self.sub_window.show()

    def open_preprocess(self):
        self.sub_window = QWidget()
        self.sub_window.setWindowTitle("전처리")
        self.sub_window.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()
        label = QLabel("전처리할 녹화 폴더를 선택하세요")

        btn_select = QPushButton("폴더 선택")
        self.selected_folder = None

        def choose_folder():
            folder = QFileDialog.getExistingDirectory(self, "녹화 폴더 선택")
            if folder:
                self.selected_folder = folder
                label.setText(f"✅ 선택된 폴더:\n{os.path.basename(folder)}")

        btn_select.clicked.connect(choose_folder)

        btn_start = QPushButton("전처리 시작")
        log_area = QTextEdit()
        log_area.setReadOnly(True)
        log_area.setMaximumHeight(100)
        log_area.setText("로그: 대기 중...")

        def run_preprocess():
            if not self.selected_folder:
                log_area.setText("❌ 오류: 폴더를 선택하세요")
                return
            try:
                subprocess.run(["python", "modules/preprocessor/preprocess_qwen.py", self.selected_folder], check=True)
                log_area.setText(f"✅ 전처리 성공!\n\n🟢 음성 분석 완료")
            except Exception as e:
                log_area.setText(f"❌ 실패: {str(e)}")

        btn_start.clicked.connect(run_preprocess)

        layout.addWidget(label)
        layout.addWidget(btn_select)
        layout.addWidget(btn_start)
        layout.addWidget(log_area)
        self.sub_window.setLayout(layout)
        self.sub_window.show()

    def open_learn(self):
        self.sub_window = QWidget()
        self.sub_window.setWindowTitle("학습")
        self.sub_window.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()
        label = QLabel("학습할 전처리 완료 폴더를 선택하세요")

        btn_select = QPushButton("폴더 선택")
        self.selected_folder = None

        def choose_folder():
            folder = QFileDialog.getExistingDirectory(self, "학습 폴더 선택")
            if folder:
                self.selected_folder = folder
                label.setText(f"✅ 선택된 폴더:\n{os.path.basename(folder)}")

        btn_select.clicked.connect(choose_folder)

        btn_start = QPushButton("학습 시작")
        log_area = QTextEdit()
        log_area.setReadOnly(True)
        log_area.setMaximumHeight(100)
        log_area.setText("로그: 대기 중...")

        def run_learn():
            if not self.selected_folder:
                log_area.setText("❌ 오류: 폴더를 선택하세요")
                return
            try:
                subprocess.run(["python", "modules/learner/extract_rules.py", self.selected_folder], check=True)
                log_area.setText("✅ 학습 완료!\n\n🟢 rules_final.json 생성됨")
            except Exception as e:
                log_area.setText(f"❌ 학습 실패:\n{str(e)}")

        btn_start.clicked.connect(run_learn)

        layout.addWidget(label)
        layout.addWidget(btn_select)
        layout.addWidget(btn_start)
        layout.addWidget(log_area)
        self.sub_window.setLayout(layout)
        self.sub_window.show()

    def open_settings(self):
        self.settings_window = QWidget()
        self.settings_window.setWindowTitle("기타 설정")
        self.settings_window.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()
        btn_voice = QPushButton("🎤 음성 인식 시작")
        status_label = QLabel("상태: 대기 중")

        def start_voice():
            try:
                from modules.utils.voice_listener import start_listening
                start_listening()
                status_label.setText("🟢 음성 인식 실행 중")
            except Exception as e:
                status_label.setText(f"🔴 실패: {str(e)}")

        btn_voice.clicked.connect(start_voice)
        layout.addWidget(btn_voice)
        layout.addWidget(status_label)
        self.settings_window.setLayout(layout)
        self.settings_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())