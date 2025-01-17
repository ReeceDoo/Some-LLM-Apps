import pandas as pd
import streamlit as st
from csv_data_processor.utils import dataframe_agent
import os

def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

st.title("💡 CSV数据分析智能工具")

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
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_key = st.secrets["OPENAI_API_KEY"]


data = st.file_uploader("上传你的数据文件（CSV格式）：", type="csv")
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

query = st.text_area("请输入你关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：")
button = st.button("生成回答")

if button and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")
if button and "df" not in st.session_state:
    st.info("请先上传数据文件")
if button and openai_api_key and "df" in st.session_state:
    with st.spinner("AI正在思考中，请稍等..."):
        response_dict = dataframe_agent(openai_api_key, st.session_state["df"], query)
        if "answer" in response_dict:
            st.write(response_dict["answer"])
        if "table" in response_dict:
            st.table(pd.DataFrame(response_dict["table"]["data"],
                                  columns=response_dict["table"]["columns"]))
        if "bar" in response_dict:
            create_chart(response_dict["bar"], "bar")
        if "line" in response_dict:
            create_chart(response_dict["line"], "line")
        if "scatter" in response_dict:
            create_chart(response_dict["scatter"], "scatter")
