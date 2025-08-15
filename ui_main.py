# ui_main.py
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
)
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
    def open_settings(self): self.open_window("기타 설정")

    def open_window(self, title):
        self.sub_window = SubWindow(title)
        self.sub_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())