import streamlit as st
import openai
import re

# セッション履歴を初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# OpenAI APIキー（環境変数やSecretsに入れてください）
openai.api_key = st.secrets["openai_api_key"]

st.title("📚 AI教材室Bot（完全版）")

mode = st.radio("機能を選択", ["資料PDF表示", "生徒の質問に答えるAI", "数式・計算", "イメージ生成（DALL・E）"])

if mode == "生徒の質問に答えるAI":
    st.header("💡 生徒の質問に答えるAI")
    user_question = st.text_input("生徒の質問を入力してください")

    if user_question:
        # 履歴にユーザーの発言を追加
        st.session_state.messages.append({"role": "user", "content": user_question})

        # GPT呼び出し（履歴ごと渡す）
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたはやさしく、わかりやすく教える先生です。数式はLaTeX形式（$...$ または \[...\]）で必ず記述してください。"}
            ] + st.session_state.messages
        )

        ai_reply = response["choices"][0]["message"]["content"]

        # 履歴にAIの発言を追加
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    # これまでの会話を表示
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write(f"**あなた:** {msg['content']}")
        else:
            # LaTeX部分を検出して分割表示
            parts = re.split(r'(\$.*?\$|\\\[.*?\\\])', msg["content"]) 
            for part in parts:
                if part.startswith("$") and part.endswith("$"):
                    st.latex(part.strip("$"))
                elif part.startswith("\\[") and part.endswith("\\]"):
                    st.latex(part.strip("\\[ \\"]"))
                else:
                    st.write(part)

elif mode == "資料PDF表示":
    st.header("📄 教材PDF表示")
    st.write("教材PDFファイルをアップロードしてください")
    st.file_uploader("PDFファイル", type="pdf")

elif mode == "数式・計算":
    st.header("📐 数式・計算モード")
    st.write("ここは将来の拡張予定です")

elif mode == "イメージ生成（DALL・E）":
    st.header("🎨 イメージ生成モード")
    st.write("ここは将来の拡張予定です")
