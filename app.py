import streamlit as st
import openai
import re
from PyPDF2 import PdfReader

# ——————————————————————————————
# 1. ページ＆APIキー設定
# ——————————————————————————————
st.set_page_config(page_title="AI 教材室Bot（完全版）", layout="wide")
openai.api_key = st.secrets["openai_api_key"]

# ——————————————————————————————
# 2. サイドバーで機能選択
# ——————————————————————————————
mode = st.sidebar.radio(
    "機能を選択",
    [
        "📄 教材PDF表示",
        "💬 生徒の質問に答えるAI",
        "🧮 数式・計算",
        "🎨 イメージ生成 (DALL·E)",
    ],
)

# ——————————————————————————————
# 3. 教材PDF表示
# ——————————————————————————————
if mode == "📄 教材PDF表示":
    st.title("📄 教材PDF表示")
    uploaded_file = st.file_uploader("教材PDFファイルをアップロードしてください", type="pdf")
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() or "" + "\n"
        st.text_area("📖 PDF内容", full_text, height=400)

# ——————————————————————————————
# 4. 生徒の質問に答えるAI（完全対話＋LaTeX強化）
# ——————————————————————————————
elif mode == "💬 生徒の質問に答えるAI":
    st.title("💬 生徒の質問に答えるAI")

    # セッションステートに履歴を保持
    if "history" not in st.session_state:
        st.session_state.history = [
            {
                "role": "system",
                "content": (
                    "あなたはやさしく、わかりやすく教える先生です。"
                    "数学や理科など数式を含む場合は必ず LaTeX モード（$…$）で記述してください。"
                    "外側の `[` や `{}` は不要です。"
                ),
            }
        ]

    # ユーザー入力
    user_msg = st.chat_input("生徒の質問を入力してください")
    if user_msg:
        st.session_state.history.append({"role": "user", "content": user_msg})

        # GPT 呼び出し（過去のやりとりを丸ごと渡す）
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.history,
        )
        assistant_msg = response.choices[0].message.content
        st.session_state.history.append(
            {"role": "assistant", "content": assistant_msg}
        )

    # 履歴を吹き出し表示
    st.divider()
    st.subheader("🧭 これまでのやりとり")
    for msg in st.session_state.history[1:]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            # LaTeX 部分を自動で判定して Markdown 出力
            st.chat_message("assistant").markdown(msg["content"])

# ——————————————————————————————
# 5. 数式・計算（WolframAlpha風 簡易版）
# ——————————————————————————————
elif mode == "🧮 数式・計算":
    st.title("🧮 数式・計算")
    expr = st.text_input("計算したい式を入力してください（例: 2+3*5 や sqrt(16)）")
    if expr:
        with st.spinner("計算中..."):
            try:
                # 危険な eval を制限付きで
                result = eval(
                    expr,
                    {"__builtins__": {}},
                    {"sqrt": lambda x: x**0.5},
                )
                st.write(f"**結果**: {result}")
            except Exception as e:
                st.error(f"計算エラー: {e}")

# ——————————————————————————————
# 6. イメージ生成 (DALL·E)
# ——————————————————————————————
elif mode == "🎨 イメージ生成 (DALL·E)":
    st.title("🎨 イメージ生成 (DALL·E)")
    prompt = st.text_input("イメージを説明してください（例: 地球と月の距離のイメージ）")
    if st.button("生成"):
        with st.spinner("生成中..."):
            try:
                img_resp = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512",
                )
                url = img_resp["data"][0]["url"]
                st.image(url, caption=prompt)
            except Exception as e:
                st.error(f"生成エラー: {e}")
