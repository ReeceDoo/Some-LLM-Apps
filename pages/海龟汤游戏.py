import os
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from haiguitang_gamehost.utils import haiguitang_gamehost
import streamlit as st

from haiguitang_gamehost.prompt_template import haiguitang_system_template
from haiguitang_gamehost.haiguitang import haiguitang_txt

st.title("海龟汤游戏主持")

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
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_key = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "ai", 
                                     "content": "准备好开始\"海龟汤\"游戏了吗？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

user_prompt = st.chat_input()

if user_prompt:
    if not openai_api_key:
        st.error("📝 本工具使用OpenAI API进行游戏，需要输入API密钥。")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": user_prompt})
    st.chat_message("human").write(user_prompt)

    with st.spinner("正在思考……"):
        response = haiguitang_gamehost(user_prompt, openai_api_key)
    
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)