# ✅ AI 教材室 Bot まるっと完全統合版 (PDF読込 + AI質問応答 + Googleシート記録)

import streamlit as st
import openai
import PyPDF2
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# -------------------- 設定 ----------------------
st.set_page_config(page_title="AI 教材室 Bot (完全版)")
st.title("📚 AI 教材室 Bot （完全版）")

# OpenAI APIキー（StreamlitのSecretsから取得）
openai.api_key = st.secrets["openai_api_key"]

# Google Sheets 認証
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your-service-account.json', scope)
client = gspread.authorize(creds)
sheet = client.open("AI教材学習記録").worksheet("学習ログ")

# ---------------- PDFアップロード ----------------
st.header("📖 教材PDF表示")
uploaded_file = st.file_uploader("教材PDFをアップロードしてください", type=["pdf"])
pdf_text = ""

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() + "\n"
    st.write("--- 教材内容 ---")
    st.write(pdf_text)

# ---------------- 生徒の質問に答えるAI ----------------
st.header("💬 生徒の質問に答えるAI")
student_name = st.text_input("生徒のお名前を入力してください")
material_name = uploaded_file.name if uploaded_file else "未設定教材"
page_number = st.text_input("ページ番号を入力してください (例: P.12)")
question = st.text_input("生徒の質問を入力してください")

if st.button("AIに質問する") and question:
    try:
        context = f"以下は教材の内容です。\n{pdf_text}\n\n生徒の質問: {question}"
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "あなたは優しい先生です。"},
                      {"role": "user", "content": context}]
        )
        answer = response["choices"][0]["message"]["content"]
        st.write("### 🧠 AIの答え")
        st.write(answer)

        # Google Sheetsへ記録
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([student_name, now, material_name, page_number, question, answer, ""])
        st.success("記録しました！")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

# ---------------- 数式計算・イメージ生成(オプション) ----------------
st.header("🧮 数式・計算 (簡易版)")
math_question = st.text_input("計算したい式を入力してください (例: sqrt(16) や 2+3*5)")

if st.button("計算する") and math_question:
    try:
        result = eval(math_question)
        st.write("計算結果:", result)
    except:
        st.write("計算エラーです。式を確認してください。")

st.header("🎨 イメージ生成（DALL·E）")
prompt = st.text_input("イメージを説明してください (例: 満開の桜のイメージ)")

if st.button("イメージを生成する") and prompt:
    try:
        dalle_response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256"
        )
        st.image(dalle_response['data'][0]['url'])
    except Exception as e:
        st.error(f"エラー: {e}")
