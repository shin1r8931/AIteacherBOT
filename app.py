import streamlit as st
import openai
import re
from datetime import datetime

# OpenAI APIキー（StreamlitのSecretsから取得）
openai.api_key = st.secrets["openai_api_key"]

st.set_page_config(page_title="AI教材室 Bot（完全対話＋LaTeX対応版）")
st.title("📚 AI教材室 Bot（完全版）")
st.header("🧠 生徒の質問に答えるAI")

# セッション履歴を初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# ユーザーの入力
user_input = st.text_input("生徒の質問を入力してください", "")

# ユーザー入力があれば履歴に追加
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # OpenAIへのリクエスト用履歴（systemプロンプト + ユーザーとAIの履歴）
    prompt_messages = [
        {"role": "system", "content": "あなたはやさしく、わかりやすく教える先生です。数学や理科などの数式は必ずLaTeX形式（$ ... $ で囲む）で記述してください。分数、べき乗、掛け算などもLaTeXを使い、簡単な数値は文章でも良いですが、数式はLaTeXが優先です。"}
    ] + st.session_state.messages

    # GPT呼び出し
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=prompt_messages
    )

    ai_response = response.choices[0].message["content"]

    # AIの返答も履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# --- 表示部 ---

st.write("---")
st.subheader("📝 これまでのやりとり")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**🧑 生徒:** {msg['content']}")
    else:
        # LaTeX数式の自動検出と表示
        parts = re.split(r'(\$.*?\$)', msg['content'])
        for part in parts:
            if re.match(r'^\$.*\$$', part):
                st.latex(part.strip("$"))
            else:
                st.write(part)

# ログ保存（オプション）
if st.button("📥 ログをダウンロードする"):
    log_text = "\n".join([
        f"[{datetime.now()}] {m['role']} -> {m['content']}" for m in st.session_state.messages
    ])
    st.download_button("Download Log", log_text, file_name="chat_log.txt")
