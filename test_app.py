# import streamlit as st
# import hgtk  # 한글 자모 분리를 위한 라이브러리 (pip install hgtk)
# from _def import ask_gpt  # GPT 호출 함수 불러오기
#
# # 🔹 Streamlit 설정
# st.set_page_config(page_title="무한워들", layout="centered")
#
# # 🔹 난이도 선택 (세트 시작 시 한 번만 설정)
# st.title("🎮 무한 워들 🎮")
#
# if "difficulty" not in st.session_state:
#     st.session_state.difficulty = st.radio("난이도를 선택하세요:", ["초급", "중급", "고급"])
#
# # 🔹 세트 시작: 단어 5개 불러오기
# if "words" not in st.session_state:
#     words, hints = ask_gpt(st.session_state.difficulty)
#
#     # 🔹 "단어1: " 같은 부분 제거 (여기서 한번 더 확인)
#     words = [word.split(":")[-1].strip() if ":" in word else word for word in words]
#
#     st.session_state.words = words
#     st.session_state.hints = hints
#     st.session_state.phoneme_counts = [len(hgtk.text.decompose(word).replace("ᴥ", "")) for word in words]
#     # # 🔹 디버깅: Streamlit에서 결과 확인
#     # st.write("✅ 단어 리스트 (가공 후):", words)
#     # st.write("✅ 힌트 리스트:", hints)
#     # st.write("✅ 음소 개수 리스트:", st.session_state.phoneme_counts)
#     st.session_state.current_word_index = 0  # 현재 맞추고 있는 단어 인덱스
#     st.session_state.attempts = 6  # 각 단어당 시도 횟수
#     st.session_state.score = 0  # 세트 총 점수
#     st.session_state.hint_used = False  # 힌트 사용 여부
#
# # 🔹 현재 단어 정보
# current_word = st.session_state.words[st.session_state.current_word_index]
# current_hint = st.session_state.hints[st.session_state.current_word_index]
# phoneme_count = st.session_state.phoneme_counts[st.session_state.current_word_index]
# word_jamos = list(hgtk.text.decompose(current_word).replace("ᴥ", ""))  # 정답 단어의 자모 분리
#
# st.write(f"📝 **{st.session_state.current_word_index + 1}/5 번째 단어**를 맞춰보세요!")
# st.write(f"💡 힌트: {current_hint} (음소 개수: {phoneme_count})")
#
# # 🔹 단어 입력
# user_input = st.text_input("단어 입력:", key="user_input")
#
# if st.button("확인"):
#     if user_input == "":
#         st.warning("⚠️ 단어를 입력해주세요!")
#     else:
#         user_jamos = list(hgtk.text.decompose(user_input).replace("ᴥ", ""))
#
#         if len(user_jamos) != phoneme_count:
#             st.warning(f"⚠️ 입력한 단어의 음소 개수는 {len(user_jamos)}개입니다. 정확히 {phoneme_count}개인 단어를 입력하세요!")
#         else:
#             # 🔹 피드백 생성 (🟩🟨🟥 유지)
#             feedback = []
#             for i in range(len(word_jamos)):
#                 if user_jamos[i] == word_jamos[i]:  # 정확한 위치 (초록색)
#                     feedback.append("🟩")
#                 elif user_jamos[i] in word_jamos:  # 포함되지만 위치 다름 (노란색)
#                     feedback.append("🟨")
#                 else:  # 아예 존재하지 않음 (빨간색)
#                     feedback.append("🟥")
#
#             # 🔹 결과 출력
#             st.write(f"단어: {' '.join(user_jamos)}")
#             st.write(f"결과: {' '.join(feedback)}")
#
#             # 🔹 정답 체크
#             if user_jamos == word_jamos:
#                 earned_score = (6 - st.session_state.attempts) * 10 + 10  # 점수 계산
#                 st.session_state.score += earned_score
#                 st.success(f"🎉 정답입니다! ({earned_score}점 획득)")
#
#                 if st.session_state.current_word_index < 4:  # 다음 단어로 이동
#                     st.session_state.current_word_index += 1
#                     st.session_state.attempts = 6  # 시도 횟수 초기화
#                 else:  # 5개 단어를 모두 맞춘 경우
#                     st.success(f"🎯 세트 종료! 총 점수: {st.session_state.score}점")
#                     st.session_state.words = None  # 게임 리셋
#
#             else:
#                 st.session_state.attempts -= 1
#                 if st.session_state.attempts == 0:
#                     st.error(f"❌ 실패! 정답은 '{current_word}'였습니다.")
#                     if st.session_state.current_word_index < 4:
#                         st.session_state.current_word_index += 1
#                         st.session_state.attempts = 6
#                     else:
#                         st.success(f"🎯 세트 종료! 총 점수: {st.session_state.score}점")
#                         st.session_state.words = None  # 게임 리셋
#
# st.write(f"🔢 남은 기회: {st.session_state.attempts}회 | 🎯 현재 점수: {st.session_state.score}점")
#
#
import streamlit as st
import hgtk  # 한글 자모 분리를 위한 라이브러리 (pip install hgtk)
from _def import ask_gpt  # GPT 호출 함수 불러오기

# 🔹 Streamlit 설정
st.set_page_config(page_title="무한워들", layout="wide")  # 🔹 화면을 넓게 사용

# 🔹 난이도 선택 (세트 시작 시 한 번만 설정)
st.title("🎮 무한 워들 🎮")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = st.radio("난이도를 선택하세요:", ["초급", "중급", "고급"])


# 🔹 세트 시작: 단어 5개 불러오기
if "words" not in st.session_state:
    words, hints = ask_gpt(st.session_state.difficulty)

    # 🔹 "단어1: " 같은 부분 제거
    words = [word.split(":")[-1].strip() if ":" in word else word for word in words]

    st.session_state.words = words
    st.session_state.hints = hints
    st.session_state.phoneme_counts = [len(hgtk.text.decompose(word).replace("ᴥ", "")) for word in words]

    # 🔹 게임 진행 정보 초기화
    st.session_state.current_word_index = 0  # 현재 맞추고 있는 단어 인덱스
    st.session_state.attempts = 6  # 각 단어당 시도 횟수
    st.session_state.score = 0  # 세트 총 점수
    st.session_state.hint_used = False  # 힌트 사용 여부
    st.session_state.history = []  # 입력 기록 저장 리스트

# 🔹 현재 단어 정보
current_word = st.session_state.words[st.session_state.current_word_index]
current_hint = st.session_state.hints[st.session_state.current_word_index]
phoneme_count = st.session_state.phoneme_counts[st.session_state.current_word_index]
word_jamos = list(hgtk.text.decompose(current_word).replace("ᴥ", ""))  # 정답 단어의 자모 분리

# 🔹 현재 난이도 표시 (큰 글씨)
st.markdown(f"## 🔥 현재 난이도: **{st.session_state.difficulty}**")
st.markdown(f"### 🎯 현재 점수: **{st.session_state.get('score', 0)}점**")



# 🔹 화면을 왼쪽(게임 진행), 오른쪽(입력 기록)으로 나누기
col1, col2 = st.columns([2, 1])

# 🔹 왼쪽: 게임 진행 UI
with col1:
    st.write(f"📝 **{st.session_state.current_word_index + 1}/5 번째 단어**를 맞춰보세요!")
    st.write(f"💡 힌트: {current_hint} (음소 개수: {phoneme_count})")

    # 🔹 단어 입력
    user_input = st.text_input("단어 입력:", key="user_input")

    if st.button("확인"):
        if user_input == "":
            st.warning("⚠️ 단어를 입력해주세요!")
        else:
            user_jamos = list(hgtk.text.decompose(user_input).replace("ᴥ", ""))

            if len(user_jamos) != phoneme_count:
                st.warning(f"⚠️ 입력한 단어의 음소 개수는 {len(user_jamos)}개입니다. 정확히 {phoneme_count}개인 단어를 입력하세요!")
            else:
                # 🔹 피드백 생성 (🟩🟨🟥 유지)
                feedback = []
                for i in range(len(word_jamos)):
                    if user_jamos[i] == word_jamos[i]:  # 정확한 위치 (초록색)
                        feedback.append("🟩")
                    elif user_jamos[i] in word_jamos:  # 포함되지만 위치 다름 (노란색)
                        feedback.append("🟨")
                    else:  # 아예 존재하지 않음 (빨간색)
                        feedback.append("🟥")

                # 🔹 결과 출력
                st.write(f"입력한 단어: {' '.join(user_jamos)}")
                st.write(f"결과: {' '.join(feedback)}")

                # 🔹 입력 기록 저장
                st.session_state.history.append({"word": " ".join(user_jamos), "feedback": " ".join(feedback)})

                # 🔹 정답 체크
                if user_jamos == word_jamos:
                    earned_score = (6 - st.session_state.attempts) * 10 + 10  # 점수 계산
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

    st.write(f"🔢 남은 기회: {st.session_state.attempts}회 | 🎯 현재 점수: {st.session_state.score}점")

# 🔹 오른쪽: 입력 기록 표시
with col2:
    st.markdown("## 📜 입력 기록")

    if st.session_state.history:
        for entry in reversed(st.session_state.history):  # 최신 입력이 위에 오도록
            st.write(f"**입력:** {entry['word']}")
            st.write(f"**결과:** {entry['feedback']}")
            st.markdown("---")  # 구분선 추가
    else:
        st.write("아직 입력한 단어가 없습니다.")
