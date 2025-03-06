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
def ask_gpt(prompt):
    """GPT-4o 모델을 사용하여 질문에 대한 답변을 생성하는 함수"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """당신은 한국어 단어 맞히기 게임을 위한 AI입니다.  
            자음과 모음 개수를 합쳐서 정확히 6개인 한 단어를 선정하고, 이에 대한 간단한 힌트를 제공합니다.
             
             ### 단어 선정 예시 ###
            예시:
            단어: 안녕 / 힌트: 사람과 사람이 만났을 때 하거나 헤어질 때 하는 인사
            단어: 안정 / 힌트: 마음이나 상태가 편안하고 조용한 상태
            단어: 심장 / 힌트: 몸의 중요한 장기 중 하나
             
             ### 출력 형식 ###
            반드시 단어와 힌트만 '단어: xxx / 힌트: xxx' 형식으로 답변하세요."""},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()



def ask_gpt(difficulty):
    """
    GPT-4o 모델을 사용하여 자음+모음이 6개인 단어와 난이도별 힌트를 생성하는 함수.
    
    difficulty (str): 초급, 중급, 고급 난이도 선택
    """
    prompt = f"""
    당신은 한국어 단어 맞히기 게임을 위한 AI입니다.  
    자음과 모음 개수를 합쳐서 정확히 6개인 한 단어를 선정하고, 이에 대한 힌트를 제공합니다.
    난이도는 초급, 중급, 고급으로 나뉩니다.

### 단어, 힌트 선정 예시 ###
단어: 안정 / 초급 힌트: 마음이나 상태가 편안하고 조용한 상태 / 중급 힌트 : 힘들때 필요한 것 / 고급 힌트: 쉼과 관련


### 난이도 ###
- 초급: 해당 단어를 명확하게 설명
- 중급: 짧고 유추하기 어려운 힌트 제공
- 고급: 해당 단어와 유사한 단어 1개를 제공하여 추론이 필요한 힌트 제공

### 출력 형식 ###
반드시 단어와 힌트만 '단어: xxx / 힌트: xxx' 형식으로 답변하세요."""
    

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"자음+모음이 6개인 한국어 단어와 {difficulty} 수준의 힌트를 하나 선정해줘."}
        ]
    )

    # GPT 응답 파싱
    ai_output = response.choices[0].message.content.strip()
    try:
        word, hint = ai_output.split(" / ")
        word = word.replace("단어:", "").strip()
        hint = hint.replace("힌트:", "").strip()
        return word, hint
    except:
        return None, None  # 형식 오류 시 None 반환