import streamlit as st

from langchain.memory import ConversationBufferMemory
from utils import qa_agent
import os


st.title("📑 AI智能PDF问答工具")

# with st.sidebar:
#     openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
#     st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

# 是否使用免费API
if "free_api" not in st.session_state:
    st.session_state.free_api = False

with st.sidebar:
    openai_api_key = st.text_input("🔑 请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
    # free_api_button = st.button("使用免费API", on_click=lambda: st.write("已使用免费API！"))
    free_api_button = st.button("使用免费API")
    if free_api_button and not st.session_state.free_api:
        st.session_state.free_api = True
    if openai_api_key:
        st.session_state.free_api = False

# 如果使用免费API，从环境变量中获取API密钥    
if st.session_state.free_api:
    # st.markdown("*🔑 正在使用免费API*")
    # 提示
    st.warning("🔑 正在使用免费API")
    openai_api_key = os.getenv("OPENAI_API_KEY")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )

uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")
question = st.text_input("对PDF的内容进行提问", disabled=not uploaded_file)

if uploaded_file and question and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")

if uploaded_file and question and openai_api_key:
    with st.spinner("AI正在思考中，请稍等..."):
        response = qa_agent(openai_api_key, st.session_state["memory"],
                            uploaded_file, question)
    st.write("### 答案")
    st.write(response["answer"])
    st.session_state["chat_history"] = response["chat_history"]

if "chat_history" in st.session_state:
    with st.expander("历史消息"):
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.write(human_message.content)
            st.write(ai_message.content)
            if i < len(st.session_state["chat_history"]) - 2:
                st.divider()
