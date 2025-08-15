Tobbalc - Koc 자율 게임봇
"사용자가 가르치면, 봇이 진화한다"

오프라인, 경량화, 한국어 최적화 게임 자동화 봇  
사용자의 음성 + 키보드 + 화면 녹화 → 학습 → 자율 행동

## ✅ 기능
- [x] UI 기반 제어 (PySide6)
- [x] 화면 + 음성 + 키보드 동시 녹화
- [ ] 음성 보정 (Vosk / Qwen)
- [ ] 자연어 → 규칙 추출 (Ollama + qwen:7b)
- [ ] 자율 게임봇 실행

## 📦 설치

```bash
git clone https://github.com/oninepa/tobbalc.git
cd tobbalc
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt