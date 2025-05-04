# 📦 完全まるっと版（Teamプラン + 共通URL + 生徒5人セッション管理 + 完全LaTeX + 対話型Bot）

import streamlit as st
import openai
import re
from datetime import datetime

# === 環境変数・APIキー ===
openai.api_key = st.secrets["openai_api_key"]

# === セッション管理（生徒名で管理） ===
st.header("📚 AI 教材室 Bot （完全版）")

# 生徒名入力（セッション名）
student_name = st.text_input("あなたの名前を入力してください（例：Aくん、Bさん など）")

if student_name:
    st.success(f"{student_name} さん、こんにちは！ 質問をどうぞ。")

    # セッション履歴を保持
    if "messages" not in st.session_state:
        st.session_state.messages = {}

    if student_name not in st.session_state.messages:
        st.session_state.messages[student_name] = []

    # === ユーザーの質問受付 ===
    user_question = st.text_input("生徒の質問を入力してください")

    if user_question:
        # 履歴に追加（ユーザー）
        st.session_state.messages[student_name].append({"role": "user", "content": user_question})

        with st.spinner("師匠が考え中..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたはやさしく、わかりやすく教える先生です。数式はLaTeXで書き、文章と組み合わせて生徒が理解しやすいように説明してください。生徒の追加質問にも丁寧に対話するBotです。"}
                ] + st.session_state.messages[student_name]
            )

            answer = response.choices[0].message["content"]

            # 履歴に追加（アシスタント）
            st.session_state.messages[student_name].append({"role": "assistant", "content": answer})

        # === LaTeX整形表示 ===
        parts = re.split(r'(\$.*?\$)', answer)
        for part in parts:
            if re.match(r'^\$.*\$$', part):
                st.latex(part.strip('$'))
            else:
                st.write(part)

    # === 過去の会話表示 ===
    st.write("---")
    st.subheader("これまでの会話")

    for msg in st.session_state.messages[student_name]:
        role = "👦 生徒" if msg["role"] == "user" else "👨‍🏫 師匠"
        st.write(f"**{role}**: {msg['content']}")

    # === ログ保存（簡易版：ログファイル出力はローカル環境用などに追加可能） ===
    # 現在はセッション中だけ保存（Streamlitのセッション）

else:
    st.warning("まずはあなたの名前を入力してください。")
