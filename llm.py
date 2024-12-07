from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

def call_llm(prompt, model="gpt-4-turbo"):
    llm = ChatOpenAI(model=model)
    return llm.invoke(prompt).content