import streamlit as st
import openai

st.title("AI 教材室 Bot（完全版）")

user_question = st.text_input("生徒の質問を入力してください")

if user_question:
    client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

    response = client.chat.completions.create(
        model="gpt-4o",  # ここは必要に応じて gpt-3.5-turbo でもOK
        messages=[
            {"role": "system", "content": "あなたはやさしい先生AIです。生徒の質問にわかりやすく答えてください。"},
            {"role": "user", "content": user_question}
        ]
    )

    st.write(response.choices[0].message.content)
