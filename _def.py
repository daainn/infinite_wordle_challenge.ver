import os
import openai
import random
import hgtk  # 한글 자모 분리를 위한 라이브러리 (pip install hgtk)
from dotenv import load_dotenv
import sys

# OpenAI API 키 설정
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key


def ask_gpt(difficulty):
    """
    GPT-4o 모델을 사용하여 자음+모음이 6개인 단어와 난이도별 힌트를 생성하는 함수.
    
    difficulty (str): 초급, 중급, 고급 난이도 선택
    """
    prompt = f"""
    당신은 한국어 단어 맞히기 게임을 위한 AI입니다.
    **자음과 모음 개수를 합쳐서 정확히 6개인** 단어를 5개를 선정하고, 이에 대한 힌트를 제공합니다.
    힌트 난이도는 초급, 중급, 고급으로 나뉘어져 있으며,
    난이도가 올라갈 수록 단어를 맞히기 어려운 힌트가 제공됩니다.

### 단어 선정 예시 ###
- **자음과 모음 개수를 합쳐 6개인 단어 5개**를 선정 해야합니다.
- 예시 ) 심장(ㅅㅣㅁㅈㅏㅇ), 바나나(ㅂㅏㄴㅏㄴㅏ), 음정(ㅇㅡㅁㅈㅓㅇ) 등 (예시로 나온 단어는 선정 금지)
- 받침이 있어도 상관없으나, **자음과 모음을 합쳐 정확히 6개가 되어야 합니다.**
- 안되는 예시) 바람(ㅂㅏㄹㅏㅁ) 5개의 음소를 가져서 탈락. 초콜릿(ㅊㅗㅋㅗㄹㄹㅣㅅ) 8개의 음소를 가져서 탈락.

### 힌트 난이도 및 예시 ###
- 초급: 해당 단어를 명확하게 설명
- 중급: 짧고 유추하기 어려운 힌트 제공
- 고급: 해당 단어와 유사한 단어 1개를 제공하여 추론이 필요한 힌트 제공

### 출력 형식 ###
반드시 아래 형식으로 출력하세요.
단어1: xx / 힌트: xxx
단어2: xx / 힌트: xxx
단어3: xx / 힌트: xxx
단어4: xx / 힌트: xxx
단어5: xx / 힌트: xxx
"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{difficulty} 수준의 단어 5개와 힌트를 제공해주세요."}
        ]
    )
    # GPT 응답 파싱
    ai_output = response.choices[0].message.content.strip()
    words, hints = [], []
    try:
        lines = ai_output.split("\n")
        for line in lines:
            word, hint = line.split(" / ")
            word = word.replace("단어:", "").strip()
            hint = hint.replace("힌트:", "").strip()
            # **단어 검증: 자음+모음 개수 합이 정확히 6개인지 확인**
            # decomposed_word = hgtk.text.decompose(word).replace("ᴥ", "")  # 한글을 자모로 분해
            # if len(decomposed_word) != 6:
            #     return None, None  # 단어가 조건을 만족하지 않으면 게임 종료

            words.append(word)
            hints.append(hint)

        return words, hints
    except:
        return None, None  # 형식 오류 시 None 반환