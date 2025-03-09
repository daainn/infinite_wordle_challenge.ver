import os
import openai
import json  # 🔹 JSON 변환을 위해 추가
from dotenv import load_dotenv

# OpenAI API 키 설정
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

def ask_gpt(difficulty):
    """
    GPT-4o 모델을 사용하여 2글자 단어 5개와 난이도별 힌트를 생성하는 함수.

    difficulty (str): 초급, 중급, 고급 난이도 선택
    """
    prompt = """
    당신은 한국어 단어 맞히기 게임을 위한 AI입니다.  
    **2글자 단어 5개**를 선정하고, 단어에 대한 힌트를 제공합니다.

    ### 단어 선정 기준 ###
    - 반드시 **2글자**여야 함.
    - 받침이 있어도 상관없음.

    ### 힌트 난이도 및 예시 ###
    - 초급: 해당 단어를 명확하게 설명
    - 중급: 짧고 유추하기 어려운 힌트 제공
    - 고급: 해당 단어와 유사한 단어 1개를 제공하여 추론이 필요한 힌트 제공

    ### 출력 형식 ###
    반드시 **JSON 형식**으로 출력하세요:
    {
        "words": ["단어1", "단어2", "단어3", "단어4", "단어5"],
        "hints": ["힌트1: xxx", "힌트2: xxx", "힌트3: xxx", "힌트4: xxx", "힌트5: xxx"]
    }
    """

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{difficulty} 수준의 단어 5개와 힌트를 제공해주세요."}
        ]
    )

    # 🔹 GPT 응답 원본 출력 (디버깅용)
    ai_output = response.choices[0].message.content.strip()
    print("🔍 GPT 응답 원본:\n", ai_output)

    try:
        # 🔹 GPT가 ```json ... ``` 형식으로 감싸면 제거
        if ai_output.startswith("```json"):
            ai_output = ai_output.replace("```json", "").replace("```", "").strip()

        # 🔹 안전하게 JSON 파싱
        parsed_output = json.loads(ai_output)

        word_list = parsed_output["words"]
        hint_list = parsed_output["hints"]

        # 🔹 "단어1: " 같은 부분 제거
        words = [word.split(":")[-1].strip() for word in word_list]
        hints = [hint.split(":")[-1].strip() for hint in hint_list]

        # 🔹 디버깅: 처리된 단어 & 힌트 출력
        print("\n✅ 처리된 단어 리스트:", words)
        print("✅ 처리된 힌트 리스트:", hints)

        # **최종 검증: 데이터가 5개씩 존재하는지 확인**
        if len(words) == 5 and len(hints) == 5:
            return words, hints
        else:
            print("❌ GPT가 올바른 개수의 데이터를 반환하지 않음:", ai_output)
            return None, None  # 잘못된 경우 None 반환

    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류 발생: {e}")
        return None, None  # JSON 변환 오류 발생 시 실패 처리

    except Exception as e:
        print(f"❌ 알 수 없는 오류 발생: {e}")
        return None, None  # 기타 오류 발생 시 실패 처리


# if __name__ == "__main__":
#     # 난이도를 테스트할 때 변경 가능
#     difficulty = "초급"
#
#     # ask_gpt() 실행하여 응답 확인
#     words, hints = ask_gpt(difficulty)
#
#     print("\n🔍 최종 반환된 데이터:")
#     print("✅ 단어 리스트:", words)
#     print("✅ 힌트 리스트:", hints)
