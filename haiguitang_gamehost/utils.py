from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from haiguitang_gamehost.prompt_template import haiguitang_system_template, haiguitang_user_template
from haiguitang_gamehost.haiguitang import haiguitang_txt

import os

DEFINE OPENAI_API_KEY

def haiguitang_gamehost(user_prompt, openai_api_key):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", haiguitang_system_template),
            ("user", haiguitang_user_template),
        ])
    # 判断openai_api_key是否为系统的环境变量/免费API
    if openai_api_key == os.getenv("OPENAI_API_KEY"):
        model = ChatOpenAI(model="gpt-4-turbo", openai_api_key=openai_api_key, openai_api_base="https://api.aigc369.com/v1")
    else:
        model = ChatOpenAI(model="gpt-4-turbo", openai_api_key=openai_api_key)
    
    chain = prompt | model
    reponse = chain.invoke({
        "haiguitang_txt": haiguitang_txt,
        "user_input": user_prompt
        })
    return reponse.content

# model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), openai_api_base="https://api.aigc369.com/v1")
# print(haiguitang_gamehost("开始", os.getenv("OPENAI_API_KEY")))
