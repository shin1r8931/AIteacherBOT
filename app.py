# app.py
import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import tempfile
import re

# ─ Streamlit の設定 ─────────────────────────────────────────
st.set_page_config(page_title="AI 教材室 Bot（完全版）", layout="wide")
st.title("📚 AI 教材室 Bot（完全版）")

# ─ OpenAI クライアントの初期化 ──────────────────────────────
# Streamlit Cloud の Secrets から読み込み
# 事前に「Settings > Secrets」に以下を登録してください:
# openai_api_key = "sk-XXXX..."
client = OpenAI(api_key=st.secrets["openai_api_key"])

# ─ サイドバーで機能切り替え ─────────────────────────────────
mode = st.sidebar.radio(
    "機能を選択",
    ["教材PDF表示", "生徒の質問に答えるAI", "数式・計算", "イメージ生成（DALL·E）"],
)

if mode == "教材PDF表示":
    st.header("📄 教材PDF表示")
    uploaded_file = st.file_uploader("教材PDFファイルをアップロードしてください", type="pdf")
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        # PDFプレビュー
        with open(tmp_path, "rb") as f:
            base64_pdf = f.read()
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf.encode("base64").decode()}" width="700" height="900" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        # 抽出テキスト表示
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        st.subheader("📑 教材PDFから抽出したテキスト")
        st.write(text)

elif mode == "生徒の質問に答えるAI":
    st.header("👂 生徒の質問に答えるAI")
    user_q = st.text_input("生徒の質問を入力してください")
    if user_q:
        with st.spinner("AI が考え中…"):
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは親切な家庭教師です。"},
                    {"role": "user", "content": user_q},
                ],
                temperature=0.5,
            )
        ai_ans = res.choices[0].message.content
        st.write(ai_ans)

elif mode == "数式・計算":
    st.header("🧮 数式・計算（簡易版）")
    expr = st.text_input("計算したい式を入力してください（例: 2+3*5）")
    if expr:
        try:
            # 危険なevalを避けるため、数字と演算子のみ簡易チェック
            if re.fullmatch(r"[0-9+\-*/(). ]+", expr):
                result = eval(expr)
                st.success(f"結果: {result}")
            else:
                st.error("数式に不正な文字が含まれています。")
        except Exception as e:
            st.error(f"計算エラー: {e}")

elif mode == "イメージ生成（DALL·E）":
    st.header("🎨 イメージ生成（DALL·E）")
    prompt = st.text_input("イメージを説明してください（例: 地球と月の距離のイメージ）")
    if prompt:
        with st.spinner("画像生成中…"):
            img_res = client.images.generate(
                prompt=prompt,
                n=1,
                size="512x512"
            )
        img_url = img_res.data[0].url
        st.image(img_url, caption=prompt)
