from llm import call_llm
from agents.complexity.websearch import websearch_agent

def tech_stack(url):
    docs = websearch_agent(url)
    response = call_llm(f"""
Find out the tech stack and packages used in this github repository {url} using the supplementary docs:
{docs}

""")
    return response