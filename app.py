import streamlit as st
from openai import OpenAI
import PyPDF2
import re

# OpenAIクライアント設定
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.title("📚 AI教材室 Bot （完全対話型版）")

# タブ作成
tabs = st.tabs(["📖 教材PDF表示", "💡 生徒の質問に答えるAI"])

# --- 📖 教材PDF表示 ---
with tabs[0]:
    pdf_file = st.file_uploader("教材PDFをアップロードしてください", type="pdf")

    if pdf_file is not None:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        st.text_area("PDF内容", text, height=400)

# --- 💡 生徒の質問に答えるAI（対話型） ---
with tabs[1]:
    st.header("生徒の質問に答えるAI")

    # セッションステートで会話履歴を保持
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # これまでの会話を表示
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write("🧑‍🎓 生徒: " + msg["content"])
        else:
            st.write("👩‍🏫 AI: " + msg["content"])

    user_question = st.text_input("生徒の質問を入力してください")

    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.spinner("考え中..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたはやさしく、わかりやすく教える先生です。数学や理科など数式を含む説明をする際は、必ず以下のLaTeX数式ルール設定テンプレに従ってください。\n\n[LaTeX数式ルール設定テンプレ]\n\n【基本ルール】\n- 数式は必ずLaTeXモードで記述し、$ ～ $ で囲ってください。\n- LaTeXの外側に [ ] や { } は不要です。streamlitでは $ ～ $ で囲むだけで正しく表示されます。\n- 分数や掛け算、べき乗表記などは、文章中でも良いですが、分数や掛け算、指数などは必ずLaTeXを使います。\n\n【数式の書き方例】\n- 分数 → $ \frac{a}{b} $\n- 掛け算 → $ a \times b $\n- 指数 → $ x^2 $\n- 三角形の面積 → $ S = \frac{1}{2} \times 底辺 \times 高さ $\n\n【文章と数式の組み合わせ】\n- 文章中に数式を入れる場合も、数式部分だけを $ ～ $ で囲んでください。\n\n例：\n三角形の面積は $ S = \frac{1}{2} \times 底辺 \times 高さ $ です。\n\n【補足】\n- 中学生レベルを超える複雑な数式や特別な記号（1/2 など）は、LaTeXと併用でもOKです。\n- ただし、可能な限りLaTeXを優先し、見た目もわかりやすく整えてください。\n- LaTeX内の特殊記号 { } や [ ] などはそのまま書いてください。\n\n以上を守って、生徒にわかりやすく整った形で数式と説明を出力してください。"}
                ] + st.session_state.messages
            )

            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})

            st.write("👩‍🏫 AI: " + answer)
