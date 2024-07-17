from xiaohongshu_generator.prompt_template import system_template_text, user_template_text
from xiaohongshu_generator.xiaohongshu_model import Xiaohongshu

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate

import os


def generate_xiaohongshu(theme, openai_api_key):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_template_text),
            ("user", user_template_text),
        ]
    )
    # 判断openai_api_key是否为系统的环境变量/免费API
    # if openai_api_key == os.getenv("OPENAI_API_KEY"):
    if openai_api_key == st.secrets["OPENAI_API_KEY"]:
        model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key, openai_api_base="https://api.aigc369.com/v1")
    else:
        model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
    
    # model = ChatOpenAI(openai_api_key=openai_api_key, openai_api_base="https://api.aigc369.com/v1")
    output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)

    chain = prompt | model | output_parser
    # chain = prompt | model
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "theme": theme
        })
    return result

