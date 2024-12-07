from llm import call_llm
from pydantic import BaseModel
from typing import List
import json
import requests
from bs4 import BeautifulSoup

class Links(BaseModel):
    links: List[str]

def find_links(text):
    prompt=f"""
From the given text, find out all the links and output them as a list
{text}

Give the output in form of json dump following the provided pydantic models:
class Links(BaseModel):
    links: List[str]

Do not output anything else.
"""
    response = call_llm(prompt)
    try:
        fin = Links(**json.loads(response[7:-3]))
        return fin.links
    except:
        return []

def find_docs(links):
    docs = []
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text(strip=True)
        docs.append(page_text)
    return docs



def websearch_agent(url):
    text = find_docs([url])
    links = find_links(text)
    docs = find_docs(links)
    return [text] + docs