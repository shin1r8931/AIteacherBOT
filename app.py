import streamlit as st
import openai
from PyPDF2 import PdfReader

# OpenAI APIキーをsecretsから取得
openai.api_key = st.secrets["openai_api_key"]

st.set_page_config(page_title="AI 教材室 Bot（完全版）", page_icon="📚")

st.title("📚 AI 教材室 Bot（完全版）")

# タブを作成
tab1, tab2, tab3, tab4 = st.tabs(["📄 教材PDF表示", "💬 生徒の質問に答えるAI", "🧮 数式・計算", "🎨 イメージ生成（DALL-E）"])

# --- 教材PDF表示 ---
with tab1:
    st.header("教材PDF表示")
    uploaded_file = st.file_uploader("教材PDFファイルをアップロードしてください", type="pdf")
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                st.write(text)

# --- 生徒の質問に答えるAI ---
with tab2:
    st.header("生徒の質問に答えるAI")
    question = st.text_input("生徒の質問を入力してください")

    if question:
        with st.spinner("AIが考え中..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "あなたは優しくてわかりやすい先生です。小学生にも分かるように簡単に答えてください。"},
                          {"role": "user", "content": question}],
            )
            st.write(response["choices"][0]["message"]["content"])

# --- 数式・計算 ---
with tab3:
    st.header("数式・計算（Wolfram Alpha風 簡易版）")
    math_question = st.text_input("計算したい式を入力してください（例: 2+3*5 や sqrt(16)）")

    if math_question:
        with st.spinner("計算中..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "あなたは優秀な計算AIです。与えられた数式を計算して、答えだけを返してください。"},
                          {"role": "user", "content": math_question}],
            )
            st.write(response["choices"][0]["message"]["content"])

# --- イメージ生成（DALL-E） ---
with tab4:
    st.header("イメージ生成（DALL-E）")
    image_prompt = st.text_input("イメージを説明してください（例: 桜の木の下で本を読む猫）")

    if image_prompt:
        with st.spinner("画像を生成中..."):
            response = openai.Image.create(
                model="dall-e-3",
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response["data"][0]["url"]
            st.image(image_url, caption=image_prompt)
