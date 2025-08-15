# extract_rules.py - Qwen을 이용해 음성+로그에서 규칙 추출
import os
import json
import subprocess
import sys

def extract_rules_from_session(folder_path):
    # 입력 파일 확인
    voice_file = os.path.join(folder_path, "voice_google.json")
    input_log = os.path.join(folder_path, "input_log.json")
    
    if not os.path.exists(voice_file):
        print("❌ 음성 파일 없음")
        return None

    with open(voice_file, "r", encoding="utf-8") as f:
        voice_data = json.load(f)

    # Qwen에 보낼 프롬프트
    prompt = f"""
다음은 게임 플레이 중 사용자가 말한 음성 인식 결과입니다.
이 내용에서 게임 전략, 행동 규칙, 아이템 우선순위 등을 추출해 JSON 형식으로 반환하세요.

예시 입력:
"체력 낮은 적한테 스킬 A 써, 자석은 꼭 줍고, 모자 쓴 애는 친구야"

예시 출력:
{{
  "rules": [
    {{
      "type": "skill",
      "skill": "A",
      "condition": "enemy.hp < 30%"
    }},
    {{
      "type": "item",
      "item": "자석",
      "action": "수집"
    }},
    {{
      "type": "relation",
      "target": "모자 쓴 캐릭터",
      "relation": "친구"
    }}
  ]
}}

지금 데이터:
{voice_data['text']}
"""

    # Ollama CLI로 Qwen 실행
    try:
        result = subprocess.run(
            ["ollama", "run", "qwen:7b"],
            input=prompt,
            text=True,
            encoding='utf-8',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 간단한 더미 규칙 (실제 파싱은 나중에)
        rules = {
            "rules": [
                {"type": "example", "description": "이 규칙은 테스트용입니다. 실제 파싱은 향후 구현"}
            ]
        }
        
        output_file = os.path.join(folder_path, "rules_raw.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 규칙 추출 완료: {output_file}")
        return rules

    except Exception as e:
        print(f"❌ Qwen 실행 실패: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_rules_from_session(sys.argv[1])
    else:
        print("사용법: python extract_rules.py [세션폴더]")