import streamlit as st
import re
from openai import OpenAI
import PyPDF2

client = OpenAI()

st.set_page_config(page_title="AI 教材室 Bot（完全版）", page_icon="📚")
st.title("📚 AI 教材室 Bot（完全版）")

tabs = st.tabs(["教材PDF表示", "生徒の質問に答えるAI", "数式・計算", "イメージ生成（DALL-E）"])

# --- 教材PDF表示 ---
with tabs[0]:
    st.header("PDF教材を表示する")
    uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            st.text_area("PDF内容", text, height=400)

# --- 生徒の質問に答えるAI ---
with tabs[1]:
    st.header("💡 生徒の質問に答えるAI")

    user_question = st.text_input("生徒の質問を入力してください")

    if user_question:
        with st.spinner("考え中..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """
あなたはやさしく、わかりやすく教える先生です。数学や理科など数式を含む説明をする際は、必ず以下のLaTeX数式ルール設定テンプレに従ってください。

【LaTeX数式ルール設定テンプレ】

[基本ルール]
- 数式は必ずLaTeXモードで記述し、$ ～ $ で囲ってください。
- LaTeX内の記号（ \\[ や \\( など）は不要です。streamlitでは $ ～ $ で囲むだけで正しく表示されます。
- 簡単な記述（分数・掛け算・べき乗など）は、文章中でも良いですが、分数や掛け算、指数などは必ずLaTeXを使います。

[数式の書き方例]
- 分数 → $ \\frac{a}{b} $
- 掛け算 → $ a \\times b $
- 指数 → $ x^2 $
- 三角形の面積 → $ S = \\frac{1}{2} \\times 底辺 \\times 高さ $

[文章と数式の組み合わせ]
- 文章中に数式を入れる場合も、数式部分だけを $ ～ $ で囲んでください。

[補足]
- 複雑すぎる数式は LaTeX でなく文章でもよいですが、できるだけLaTeX優先で。
"""},

                    {"role": "user", "content": user_question}
                ]
            )

            answer = response.choices[0].message.content

            # LaTeX部分を分離して表示
            parts = re.split(r'(\$.*?\$)', answer)
            for part in parts:
                if re.match(r'^\$.*\$$', part):
                    st.latex(part.strip('$'))
                else:
                    st.write(part)

# --- 数式・計算タブ ---
with tabs[2]:
    st.header("✏️ 数式や計算をAIに聞く")

    calc_question = st.text_input("数式・計算の質問を入力してください")

    if calc_question:
        with st.spinner("考え中..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたはやさしく、わかりやすく教える先生です。数式は必ずLaTeXモード（$ ～ $）で書いてください。"},
                    {"role": "user", "content": calc_question}
                ]
            )

            answer = response.choices[0].message.content

            parts = re.split(r'(\$.*?\$)', answer)
            for part in parts:
                if re.match(r'^\$.*\$$', part):
                    st.latex(part.strip('$'))
                else:
                    st.write(part)

# --- 画像生成（DALL-E） ---
with tabs[3]:
    st.header("🎨 画像生成 (DALL-E)")

    dalle_prompt = st.text_input("生成したい画像を説明してください")

    if dalle_prompt:
        with st.spinner("画像生成中..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=dalle_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            st.image(image_url, caption="生成された画像", use_column_width=True)
