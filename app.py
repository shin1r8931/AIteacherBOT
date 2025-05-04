import streamlit as st
import openai
import PyPDF2
import re

from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="AI教材室Bot", layout="wide")

st.title("📚 AI 教材室 Bot （完全版）")

tabs = st.tabs(["教材PDF表示", "🎓 生徒の質問に答えるAI"])

# --- 📖 PDF表示機能 ---
with tabs[0]:
    uploaded_file = st.file_uploader("PDFをアップロードしてください", type="pdf")
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        st.text_area("PDF内容", text, height=400)

# --- 🎓 生徒の質問に答えるAI ---
with tabs[1]:
    st.header("🎓 生徒の質問に答えるAI")
    user_question = st.text_input("生徒の質問を入力してください")

    if user_question:
        with st.spinner("考え中..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたはやさしく、わかりやすく教える先生です。数学の数式は必ずLaTeX数式モードで記述し、$ で囲んでください。LaTeXの外側に [ ] や { } などは付けず、直接書いてください。"},
                    {"role": "user", "content": user_question},
                ]
            )
            answer = response.choices[0].message.content

            # LaTeXの部分を自動変換（[ ] や半端なLaTeXも含めて正規化）
            # [ S = ... ] などを $S = ...$ に変換する
            answer = re.sub(r'\[\s*(.*?)\s*\]', r'$\1$', answer)

            # LaTeX部分を判定して分割表示
            parts = re.split(r'(\$.*?\$)', answer)
            for part in parts:
                if part.startswith('$') and part.endswith('$'):
                    st.latex(part.strip('$'))
                else:
                    st.write(part)
