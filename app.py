import streamlit as st
import openai
from PyPDF2 import PdfReader

# APIキー（Secretsから取得）
openai_api_key = st.secrets["openai_api_key"]

# OpenAIクライアント（新方式）
from openai import OpenAI
client = OpenAI(api_key=openai_api_key)

# タイトル
st.set_page_config(page_title="AI 教材室 Bot（完全版）")
st.title("📚 AI 教材室 Bot （完全版）")

# サイドバーのナビゲーション
page = st.sidebar.radio("ページを選んでください", ["教材PDF表示", "生徒の質問に答えるAI", "数式・計算", "イメージ生成（DALL·E）"])

# -------------------- PDF表示 --------------------
if page == "教材PDF表示":
    st.header("📖 教材PDF表示")
    pdf_file = st.file_uploader("教材PDFファイルをアップロードしてください", type="pdf")

    if pdf_file is not None:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        st.write(text)

# -------------------- 生徒の質問に答える --------------------
elif page == "生徒の質問に答えるAI":
    st.header("💬 生徒の質問に答えるAI")
    user_input = st.text_input("生徒の質問を入力してください")

    if user_input:
        with st.spinner("考え中です..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたは優しい先生です。中学生向けに、わかりやすく簡潔に説明してください。"},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_text = response.choices[0].message.content
            st.write(ai_text)

# -------------------- 数式・計算 --------------------
elif page == "数式・計算":
    st.header("🧠 数式・計算（Wolfram Alpha風 簡易版）")
    calc_input = st.text_input("計算したい式を入力してください（例: 2+3*5 や sqrt(16)）")

    if calc_input:
        with st.spinner("計算中です..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたは計算機です。与えられた数式を計算して、答えだけを返してください。"},
                    {"role": "user", "content": calc_input}
                ]
            )
            result = response.choices[0].message.content
            st.write("計算結果: ", result)

# -------------------- イメージ生成 --------------------
elif page == "イメージ生成（DALL·E）":
    st.header("🎨 イメージ生成（DALL·E）")
    image_prompt = st.text_input("イメージを説明してください（例: 満開の桜の木と青空）")

    if image_prompt:
        with st.spinner("画像を生成中です..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="512x512",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            st.image(image_url)
