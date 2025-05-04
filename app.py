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
                    {"role": "system", "content": "messages=[
    {
        "role": "system",
        "content": """
あなたはやさしく、わかりやすく教える先生です。数学や理科など数式を含む説明をする際は、必ず以下のLaTeX数式ルール設定テンプレに従ってください。

【LaTeX数式ルール設定テンプレ】

【基本ルール】
- 数式は必ずLaTeXモードで記述し、$ ～ $ で囲ってください。
- LaTeXの外側に [] や {} などは不要です。streamlitでは $ ～ $ で囲むだけで正しく表示されます。
- 簡単な表記（分数・掛け算・べき乗など）は、文章中でも良いですが、分数や掛け算、指数などは必ずLaTeXを使います。

【数式の書き方例】
- 分数 → $ \\frac{a}{b} $
- 掛け算 → $ a \\times b $
- 指数 → $ x^2 $
- 三角形の面積 → $ S = \\frac{1}{2} \\times 底辺 \\times 高さ $

【文章と数式の組み合わせ】
- 文章中に数式を入れる場合も、数式部分だけを $ ～ $ で囲んでください。

例：
三角形の面積は $ S = \\frac{1}{2} \\times 底辺 \\times 高さ $ です。

【補足】
- 中学生レベルを超える複雑な数式や特別な記号（1/2 など）は、LaTeXと併用でもOKです。
- ただし、可能な限りLaTeXを優先し、見た目もわかりやすく整えてください。
- LaTeX内の特殊記号（{} など）はそのまま記述してください。

以上を守って、生徒にも分かりやすく、整った形で数式と説明を出力してください。
"""
    },
    {
        "role": "user",
        "content": user_question
    }
]
"},
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
