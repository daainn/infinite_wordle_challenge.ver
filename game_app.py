import streamlit as st
import hgtk  # 한글 자모 분리를 위한 라이브러리 (pip install hgtk)
from _def import ask_gpt  # GPT 호출 함수 불러오기

# 🔹 Streamlit 설정
st.set_page_config(page_title="무한워들", layout="centered")

# 🔹 난이도 선택
st.title("🎮 무한 워들 🎮")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = st.radio("힌트 난이도를 선택하세요:", ["초급", "중급", "고급"])


# 🔹 세트 시작: 단어 5개 불러오기
if "words" not in st.session_state:
    st.session_state.words, st.session_state.hints = ask_gpt(st.session_state.difficulty)

    # **GPT 단어 오류 체크**
    if st.session_state.words is None:
        st.error("❌ AI가 단어를 생성하는 데 실패했습니다. 다시 실행해주세요.")
        st.stop()  # 게임 중단

    st.session_state.current_word_index = 0  # 현재 맞추고 있는 단어 인덱스
    st.session_state.attempts = 6  # 각 단어당 시도 횟수
    st.session_state.score = 0  # 세트 총 점수
    st.session_state.hint_used = False  # 힌트 사용 여부

# 체크
st.write(st.session_state.words)

current_word = st.session_state.words[st.session_state.current_word_index]
current_hint = st.session_state.hints[st.session_state.current_word_index]
word_jamos = list(hgtk.text.decompose(current_word).replace("ᴥ", ""))  # 정답 단어의 자모 분리

# 🔹 게임 진행 UI
st.write(f"📝 **{st.session_state.current_word_index + 1}/5 번째 단어**를 맞춰보세요!")
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
            st.write(f"단어: {' '.join(user_jamos)}")
            st.write(f"결과: {' '.join(feedback)}")

            if user_jamos == word_jamos:
                earned_score = (6 - st.session_state.attempts) * 10 + 10  # 남은 시도 횟수에 따른 점수 계산
                st.session_state.score += earned_score
                st.success(f"🎉 정답입니다! ({earned_score}점 획득)")

                if st.session_state.current_word_index < 4:  # 다음 단어로 이동
                    st.session_state.current_word_index += 1
                    st.session_state.attempts = 6  # 시도 횟수 초기화
                else:  # 5개 단어를 모두 맞춘 경우
                    st.success(f"🎯 세트 종료! 총 점수: {st.session_state.score}점")
                    st.session_state.words = None  # 게임 리셋

            else:
                st.session_state.attempts -= 1
                if st.session_state.attempts == 0:
                    st.error(f"❌ 실패! 정답은 '{current_word}'였습니다.")
                    if st.session_state.current_word_index < 4:
                        st.session_state.current_word_index += 1
                        st.session_state.attempts = 6
                    else:
                        st.success(f"🎯 세트 종료! 총 점수: {st.session_state.score}점")
                        st.session_state.words = None  # 게임 리셋


# 🔹 힌트 버튼
if not st.session_state.hint_used and st.button("힌트 보기"):
    st.session_state.hint_used = True
    st.info(f"💡 힌트: {current_hint}")

st.write(f"🔢 남은 기회: {st.session_state.attempts}회 | 🎯 현재 점수: {st.session_state.score}점")