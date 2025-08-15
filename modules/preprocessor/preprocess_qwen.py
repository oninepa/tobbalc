# preprocess_qwen.py - 음성 보정 및 전처리
import os
import json
import speech_recognition as sr
from pydub import AudioSegment

def load_audio_and_transcribe(folder_path):
    audio_file = os.path.join(folder_path, "voice_raw.wav")
    transcript_file = os.path.join(folder_path, "voice_google.json")
    
    if not os.path.exists(audio_file):
        print("음성 파일 없음")
        return
    
    # 더미 결과 생성 (실제 STT는 나중에)
    result = {
        "text": "이 적은 체력이 낮아요, 스킬 A를 써야 해요",
        "confidence": 0.85,
        "timestamp": "2025-04-05T14:30:00"
    }
    
    with open(transcript_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("✅ 더미 음성 인식 완료:", transcript_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        load_audio_and_transcribe(sys.argv[1])
    else:
        print("사용법: python preprocess_qwen.py [폴더경로]")