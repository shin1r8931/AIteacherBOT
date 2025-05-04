import streamlit as st
import openai
import re

# セッション履歴を初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# OpenAI APIキー（環境変数やSecretsに入れてください）
openai.api_key = st.secrets["openai_api_key"]

st.set_page_config(page_title="AI 教材室Bot（完全版）", layout="wide")
st.title("📚 AI 教材室Bot（完全版）")
st.header("🧑\u200d🎓 生徒の質問に答えるAI")

# セッション履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 質問入力
user_question = st.text_input("生徒の質問を入力してください")

if user_question:
    # 履歴にユーザーの質問を追加
    st.session_state.messages.append({"role": "user", "content": user_question})

    # GPTへ渡すメッセージ作成
    messages = [
        {"role": "system", "content": "あなたはやさしく、わかりやすく教える先生です。数学や理科など数式を含む場合はLaTeX数式モード（$ $）で必ず出力してください。"}
    ] + st.session_state.messages

    # OpenAIへ問い合わせ
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
    )

    answer = response.choices[0].message['content']

    # 履歴にAIの返答を追加
    st.session_state.messages.append({"role": "assistant", "content": answer})

# === 履歴表示 ===
st.write("---")
st.subheader("🧭 これまでのやりとり（スレッド表示）")

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**💬 生徒**: {message['content']}")
    else:
        # LaTeXと文章を分ける
        parts = re.split(r'(\$.*?\$)', message['content'])
        for part in parts:
            if part.startswith("$") and part.endswith("$"):
                # LaTeX部分
                st.latex(part.strip("$"))
            else:
                # 普通の文章
                st.write(part)
