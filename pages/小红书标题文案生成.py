import os
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import streamlit as st
from xiaohongshu_generator.utils import generate_xiaohongshu

st.title("爆款小红书AI写作助手✏")

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


theme = st.text_input("💡 请输入小红书主题：")
submit = st.button("🚀 生成小红书文案")

if submit and not openai_api_key:
    st.error("📝 本工具使用OpenAI API生成小红书文案，需要输入API密钥。")
    st.stop()

if submit and not theme:
    st.error("请先输入小红书主题！")
    st.stop()

if submit:
    with st.spinner("正在生成小红书文案……"):
        result = generate_xiaohongshu(theme, openai_api_key)
        # result = generate_xiaohongshu(theme, openai_api_key)
    st.success("小红书文案已生成！")
    col1, col2 = st.columns(2)
    with col1:
        st.write("##### 标题一：", result.titles[0])
        # st.write(result.titles[0])
        st.write("##### 标题二：", result.titles[1])
        # st.write(result.titles[1])
        st.write("##### 标题三：", result.titles[2])
        # st.write(result.titles[2])
        st.write("##### 标题四：", result.titles[3])
        # st.write(result.titles[3])
        st.write("##### 标题五：", result.titles[4])
        # st.write(result.titles[4])
    with col2:
        st.markdown("##### 📜 文案：")
        st.write(result.content)
