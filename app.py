import streamlit as st
import re
from openai import OpenAI

# ── Streamlit page config ─────────────────────────────
st.set_page_config(
    page_title="AI 教材室Bot（教育現場版）",
    layout="wide",
)

# ── OpenAI クライアント初期化 ────────────────────────────
# Streamlit Secrets に openai_api_key を登録しておいてください
client = OpenAI(api_key=st.secrets["openai_api_key"])

# ── セッション履歴の準備 ───────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── サイドバー ────────────────────────────────────────
st.sidebar.title("機能を選択")
mode = st.sidebar.radio("", ["生徒の質問に答えるAI"])

# ── メイン画面 ────────────────────────────────────────
st.title("📚 AI 教材室Bot（教育現場版）")

if mode == "生徒の質問に答えるAI":
    st.header("🎧 生徒の質問に答えるAI")
    user_input = st.text_input("生徒の質問を入力してください", key="input")

    if user_input:
        with st.spinner("考え中..."):
            # system + 過去履歴 + 今回の質問
            messages = [
                {"role": "system", "content": "あなたはやさしく、LaTeX数式も正しく表示するAI先生です。"}
            ] + st.session_state.history + [
                {"role": "user", "content": user_input}
            ]

            # GPT-4o への問い合わせ
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            answer = resp.choices[0].message.content

            # 履歴に追加
            st.session_state.history.append({"role": "user", "content": user_input})
            st.session_state.history.append({"role": "assistant", "content": answer})

    # ── スレッド表示 ─────────────────────────────────
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"**🧑‍🎓 生徒:** {msg['content']}")
        else:
            st.markdown("**👨‍🏫 AI先生:**")
            # LaTeX と通常文を分割して描画
            parts = re.split(r'(\$.*?\$)', msg["content"])
            for part in parts:
                if part.startswith("$") and part.endswith("$"):
                    st.latex(part.strip("$"))
                else:
                    st.write(part)

    # ── ログのダウンロード ───────────────────────────────
    if st.button("💾 ログをダウンロード"):
        log = "\n".join([f"{m['role']}︱{m['content']}" for m in st.session_state.history])
        st.download_button("Download chat log", log, file_name="chat_log.txt")
