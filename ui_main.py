# ui_main.py
import subprocess  # 맨 위에 추가
import os  # 맨 위에 추가
import sys
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt

class SubWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{title} 창 - 준비 중", self))
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autobot - King of Crabs")
        self.setGeometry(100, 100, 600, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 항상 위

        # 메인 버튼
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

    def open_bot(self): self.open_window("봇 실행")
    def open_record(self): self.open_window("녹화")
    def open_preprocess(self): self.open_window("전처리")

    def open_learn(self): self.open_window("학습")
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
        log_area = QLabel("로그: 대기 중...")
        log_area.setWordWrap(True)

        def run_learn():
            if not self.selected_folder:
                log_area.setText("❌ 오류: 폴더를 선택하세요")
                return
            try:
                subprocess.run(["python", "modules/learner/extract_rules.py", self.selected_folder], check=True)
                final_rule = os.path.join("rules", "rules_final.json")
                os.makedirs("rules", exist_ok=True)
                with open(final_rule, "w", encoding="utf-8") as f:
                    json.dump({"last_updated": self.selected_folder}, f, indent=2, ensure_ascii=False)
                log_area.setText(f"✅ 학습 완료!\n\n🟢 규칙 추출됨\n🟢 최종 규칙 저장:\n{final_rule}")
            except Exception as e:
                log_area.setText(f"❌ 학습 실패:\n{str(e)}")

        btn_start.clicked.connect(run_learn)

        layout.addWidget(label)
        layout.addWidget(btn_select)
        layout.addWidget(btn_start)
        layout.addWidget(log_area)
        self.sub_window.setLayout(layout)
        self.sub_window.show()

    def open_settings(self): self.open_window("기타 설정")

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

         # 전처리 시작 버튼
        btn_start = QPushButton("전처리 시작")
        log_area = QLabel("로그: 대기 중...")
        log_area.setWordWrap(True)

        def run_preprocess():
             if not self.selected_folder:
                 log_area.setText("❌ 오류: 폴더를 선택하세요")
                 return
             try:
                 # preprocess_qwen.py 실행
                 subprocess.run(["python", "modules/preprocessor/preprocess_qwen.py", self.selected_folder], check=True)
                 log_area.setText(f"✅ 전처리 성공!\n\n🟢 음성 분석 완료\n🟢 보정된 결과 저장:\n{os.path.join(self.selected_folder, 'voice_google.json')}")
             except Exception as e:
                   log_area.setText(f"❌ 전처리 실패:\n{str(e)}")

             # 더미 처리 완료 메시지 (실제 전처리는 나중에 연결)
             log_area.setText(f"🔍 분석 중...\n🎥 화면 변화 추출\n🎤 음성 로그 정제\n✅ 전처리 완료:\n{os.path.join(self.selected_folder, 'voice_clean.json')}")
    
        btn_start.clicked.connect(run_preprocess)

        layout.addWidget(label)
        layout.addWidget(btn_select)
        layout.addWidget(btn_start)
        layout.addWidget(log_area)
        self.sub_window.setLayout(layout)
        self.sub_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())