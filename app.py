import streamlit as st
import openai
from PyPDF2 import PdfReader
import tempfile
import re

st.set_page_config(page_title="AI 教材室 Bot（完全版）", layout="wide")
st.title("📚 AI 教材室 Bot（完全版）")

# OpenAI APIキー
openai.api_key = st.secrets["openai_api_key"]

# --- PDF表示パート ---
st.header("📄 教材PDF表示")

uploaded_file = st.file_uploader("教材PDFファイルをアップロードしてください", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.write("教材PDFプレビュー")
    with open(tmp_path, "rb") as f:
        base64_pdf = f.read()
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf.encode("base64").decode()}" width="700" height="900" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    reader = PdfReader(tmp_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()

    if extracted_text:
        st.subheader("📖 教材PDFから抽出したテキスト")
        st.write(extracted_text)

# --- AI チャットパート ---
st.header("💬 生徒の質問に答えるAI")

user_input = st.text_input("生徒の質問を入力してください:")

if user_input:
    with st.spinner("AIが考えています..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは優しい教育AIです。生徒の質問にわかりやすく答えてください。数式はLaTeXで返すとより良いです。"},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        st.write("AIの回答:")

        # LaTeXの式を自動で検出してst.latexで表示
        latex_pattern = r"\$(.*?)\$"
        parts = re.split(latex_pattern, answer)

        for i, part in enumerate(parts):
            if i % 2 == 0:
                st.write(part)
            else:
                st.latex(part)

# --- 計算パート ---
st.header("🧠 数式・計算（Wolfram Alpha風 簡易版）")

calc_input = st.text_input("計算したい式（例: 2+3*5 や sqrt(16)）")

if calc_input:
    with st.spinner("計算中..."):
        calc_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは数学の計算に強いAIです。結果はLaTeXで表現してください。"},
                {"role": "user", "content": calc_input}
            ]
        )
        st.write("計算結果:")
        st.latex(calc_response["choices"][0]["message"]["content"])

# --- DALL·E イラスト生成パート ---
st.header("🎨 イメージ生成（DALL·E）")

image_prompt = st.text_input("イメージを説明してください（例: 地球と月の距離のイメージ）")

if image_prompt:
    with st.spinner("イメージを生成しています..."):
        dalle_response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="512x512"
        )
        image_url = dalle_response['data'][0]['url']
        st.image(image_url, caption="生成されたイメージ")
