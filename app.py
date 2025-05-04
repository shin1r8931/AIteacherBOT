import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
import re

client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="AI 教材室 Bot（完全版）", page_icon="📚")

tabs = st.tabs(["📄 教材PDF表示", "🧑‍🎓 生徒の質問に答えるAI", "🧮 数式・計算", "🎨 イメージ生成（DALL-E）"])

# --- 📄 教材PDF表示 ---
with tabs[0]:
    st.header("教材PDF表示")
    uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        st.text_area("PDF内容", text, height=400)

# --- 🧑‍🎓 生徒の質問に答えるAI ---
with tabs[1]:
    st.header("生徒の質問に答えるAI")
    user_question = st.text_input("生徒の質問を入力してください")

    if user_question:
        with st.spinner("考え中..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたはやさしく、わかりやすく教える先生です。数学の数式は必ずLaTeXの数式モードで記述し、$ で囲んでください。LaTeXの外側に[ ] や { } などは付けず、直接書いてください。"}
                    {"role": "user", "content": user_question},
                ],
            )
            answer = response.choices[0].message.content

            # LaTeX部分を検出して分割表示
            parts = re.split(r'(\$.*?\$|\\\(.*?\\\))', answer)
            for part in parts:
                if re.match(r'^\$.*\$$|^\\\(.*\\\)$', part):
                    st.latex(part.strip('$').strip('\\(').strip('\\)'))
                else:
                    st.write(part)

# --- 🧮 数式・計算 ---
with tabs[2]:
    st.header("数式・計算 (LaTeXサポート)")
    expression = st.text_input("計算式または数式を入力してください (例: E=mc^2)")
    if expression:
        st.latex(expression)

# --- 🎨 イメージ生成（DALL-E） ---
with tabs[3]:
    st.header("イメージ生成（DALL-E）")
    dalle_prompt = st.text_input("生成したい画像の説明を入力してください")

    if dalle_prompt:
        with st.spinner("画像を生成中..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=dalle_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            st.image(image_url)
