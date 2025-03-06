import streamlit as st
import hgtk  # 한글 자모 분리를 위한 라이브러리 (pip install hgtk)
from _def import ask_gpt  # GPT 호출 함수 불러오기

# 🔹 Streamlit 설정
st.set_page_config(page_title="무한워들", layout="centered")

# 🔹 난이도 선택
st.title("🎮 무한 워들 🎮")
difficulty = st.radio("난이도를 선택하세요:", ["초급", "중급", "고급"])

# 🔹 단어 & 힌트 불러오기 (세션 상태 활용)
if "word" not in st.session_state:
    st.session_state.word, st.session_state.hint = ask_gpt(difficulty)

if not st.session_state.word:
    st.error("❌ AI가 단어를 생성하는 데 실패했습니다. 다시 실행해주세요.")
    st.stop()

word_jamos = list(hgtk.text.decompose(st.session_state.word).replace("ᴥ", ""))  # 정답 단어의 자모 분리
attempts = st.session_state.get("attempts", 6)  # 시도 횟수 (기본값 6)
hint_used = st.session_state.get("hint_used", False)  # 힌트 사용 여부
score = st.session_state.get("score", 100)  # 점수 시스템 (최대 100점)

# 🔹 게임 진행 UI
st.write("💡 AI가 단어를 선정했습니다! (힌트 사용 가능)")
st.markdown("**총 6번의 기회가 주어집니다.**")

# 🔹 단어 입력
user_input = st.text_input("단어 입력 (자음+모음 6개):", key="user_input")

if st.button("확인"):
    if user_input == "":
        st.warning("⚠️ 단어를 입력해주세요!")
    else:
        # 사용자가 입력한 단어 자모 분리
        user_jamos = list(hgtk.text.decompose(user_input).replace("ᴥ", ""))

        if len(user_jamos) != 6:
            st.warning(f"⚠️ 입력한 단어는 {len(user_jamos)}개의 음소를 가지고 있습니다. 정확히 6개인 단어를 입력하세요!")
        else:
            # 🔹 피드백 생성
            feedback = []
            for i in range(6):
                if user_jamos[i] == word_jamos[i]:  # 정확한 위치 (초록색)
                    feedback.append("🟩")
                elif user_jamos[i] in word_jamos:  # 포함되지만 위치 다름 (노란색)
                    feedback.append("🟨")
                else:  # 아예 존재하지 않음 (빨간색)
                    feedback.append("🟥")

            # 🔹 결과 출력
            st.write(f"입력한 단어: {' '.join(user_jamos)}")
            st.write(f"결과: {' '.join(feedback)}")

            # 🔹 점수 차감 및 횟수 업데이트
            attempts -= 1
            score -= 10
            st.session_state.attempts = attempts
            st.session_state.score = score

            # 🔹 정답 체크
            if user_jamos == word_jamos:
                st.success(f"🎉 정답입니다! 최종 점수: {score}점")
                st.session_state.word = None  # 게임 종료 후 단어 초기화
            elif attempts == 0:
                st.error(f"❌ 실패! 정답은 '{st.session_state.word}'였습니다. 최종 점수: {score}점")
                st.session_state.word = None

# 🔹 힌트 버튼
if not hint_used and st.button("힌트 보기"):
    st.session_state.hint_used = True
    st.session_state.score -= 20
    st.info(f"💡 힌트: {st.session_state.hint}")

# 🔹 남은 시도 횟수 출력
st.write(f"🔢 남은 기회: {st.session_state.attempts}회 | 🎯 현재 점수: {st.session_state.score}점")
