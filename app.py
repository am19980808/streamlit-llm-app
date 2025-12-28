import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# =========================
# LLMに質問する関数
# =========================
def ask_llm(user_input: str, expert_type: str) -> str:
    if expert_type == "健康の専門家":
        system_message = """
あなたは健康・医療・生活習慣に詳しい専門家です。
初心者にも分かりやすく、実生活に役立つように説明してください。
医療行為の断定は避け、一般的なアドバイスに留めてください。
"""
    elif expert_type == "観光の専門家":
        system_message = """
あなたは旅行・観光の専門家です。
観光地の魅力や楽しみ方、注意点をわかりやすく説明してください。
初心者にも優しい表現を心がけてください。
"""
    else:
        system_message = "あなたは親切なAIアシスタントです。"

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )

    chain = prompt | llm
    result = chain.invoke({"input": user_input})

    return result.content


# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="専門家AI相談アプリ", layout="centered")

st.title("🧠 専門家AI相談アプリ")
st.write("""
入力した内容に対して、選択した専門家としてAIが回答します。
""")

expert_type = st.radio(
    "専門家の種類を選択してください",
    ["健康の専門家", "観光の専門家"]
)

user_input = st.text_area(
    "質問を入力してください",
    placeholder="例：健康的な生活習慣を教えて / 京都旅行のおすすめは？"
)

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが考えています..."):
            answer = ask_llm(user_input, expert_type)

        st.subheader("💡 AIの回答")
        st.write(answer)
