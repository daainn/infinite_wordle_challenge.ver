import streamlit as st
import hgtk 
from _def import ask_gpt  
import time

# 🔹 Streamlit 설정
st.set_page_config(page_title="무한워들", layout="wide")

# 🔹 페이지 제목
st.markdown(
    """
    <h1 style='text-align: center; color: #fc380c;'>🔥 무한워들 챌린지.ver 🔥</h1>
    <h3 style='text-align: center; color: #f6c3a6;'>최대한 높은 점수를 기록해보세요!!</h3>
    """, unsafe_allow_html=True
)


# 🔹 사이드바: 난이도 선택 및 게임 규칙
selected_difficulty = st.sidebar.radio(
    "난이도를 선택하세요:",
    ["초급", "중급", "고급"],   
    key="difficulty"
)

st.sidebar.markdown("### 📝 게임 규칙", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div style='border: 2px solid gray; padding: 10px; border-radius: 10px;'>"
    "1. 단어를 맞출 때까지 최대 6번의 기회가 주어집니다.<br>"
    "2. 자모 단위로 정확한 위치는 🟩, 다른 위치이지만 자모가 존재하면 🟨, 존재하지 않는 글자는 🟥 표시됩니다.<br>"
    "3. 힌트를 보면 20점이 차감됩니다.<br>"
    "4. 총 5개의 단어를 맞추면 한 세트가 종료됩니다." 
    "</div>", unsafe_allow_html=True
)
# 🔹 세트 시작: 단어 5개 불러오기
if "words" not in st.session_state or st.session_state.words is None:
    words, hints = ask_gpt(selected_difficulty)
    words = [word.split(":")[-1].strip() if ":" in word else word for word in words]

    st.session_state.words = words
    st.session_state.hints = hints
    st.session_state.phoneme_counts = [len(hgtk.text.decompose(word).replace("ᴥ", "")) for word in words]
    st.session_state.current_word_index = 0
    st.session_state.attempts = 6
    st.session_state.score = 0
    st.session_state.hint_used = False
    st.session_state.history = []
    st.session_state.show_hint = False
    st.session_state.show_result = False

if st.session_state.current_word_index >= 5:
    st.markdown("### 🎯 게임이 종료되었습니다!")
    st.markdown(f"**총 점수: {st.session_state.score}점**")


    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 새로운 게임 시작"):
            st.session_state.words = None
            st.session_state.current_word_index = 0
            st.session_state.score = 0
            st.rerun()

else:
    current_word = st.session_state.words[st.session_state.current_word_index]
    current_hint = st.session_state.hints[st.session_state.current_word_index]
    phoneme_count = st.session_state.phoneme_counts[st.session_state.current_word_index]
    word_jamos = list(hgtk.text.decompose(current_word).replace("ᴥ", ""))

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### 🔥 현재 난이도: **{selected_difficulty}** 🎯 현재 점수: **{st.session_state.get('score', 0)}점**")
    
        st.write(f"📝 **{st.session_state.current_word_index + 1}/5 번째 단어**를 맞춰보세요!")
        st.write(f"🔢 남은 기회: {st.session_state.attempts}회    ✅ 음소 개수: {phoneme_count}")

        if st.session_state.show_hint:
            st.write(f"💡 힌트: {current_hint} (음소 개수: {phoneme_count})")
        else:
            if st.button("🔍 힌트 보기 (20점 차감)"):
                st.session_state.show_hint = True
                st.session_state.score = max(0, st.session_state.score - 20)
                st.rerun()
        
        user_input = st.text_input("단어 입력:", key="user_input")

        if st.button("확인"):
            if user_input == "":
                st.warning("⚠️ 단어를 입력해주세요!")
            else:
                user_jamos = list(hgtk.text.decompose(user_input).replace("ᴥ", ""))
                if len(user_jamos) != phoneme_count:
                    st.warning(f"⚠️ 입력한 단어의 음소 개수는 {len(user_jamos)}개입니다. 정확히 {phoneme_count}개인 단어를 입력하세요!")
                else:
                    feedback = ["🟩" if user_jamos[i] == word_jamos[i] else "🟨" if user_jamos[i] in word_jamos else "🟥" for i in range(len(word_jamos))]
                    st.session_state.history.append({"word": " ".join(user_jamos), "feedback": " ".join(feedback)})
                    st.session_state.attempts -= 1
                    
                    if user_jamos == word_jamos or st.session_state.attempts <= -1:
                        earned_score = (st.session_state.attempts) * 10 + 10 if user_jamos == word_jamos else 0
                        st.session_state.score += earned_score
                        if user_jamos == word_jamos:
                            st.success(f"🎉 정답입니다! ({earned_score}점 획득)")
                        else:
                            st.error(f"❌ 실패! 정답은 '{current_word}'였습니다.")
                        st.session_state.show_result = True
                        time.sleep(1.5)
                        st.session_state.current_word_index += 1
                        st.session_state.attempts = 6
                        st.session_state.show_hint = False
                        st.session_state.show_result = False
                        st.session_state.history.clear()
                        st.rerun()
    
                    
    
    with col2:
        st.markdown("### 📜 단어 입력 기록")
        if st.session_state.history:
            for entry in st.session_state.history:
                st.write(f"**입력:** {entry['word']}")
                st.write(f"**결과:** {entry['feedback']}")
