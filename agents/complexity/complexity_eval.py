from llm import call_llm
from agents.complexity.tech_stack import tech_stack

def complexity(pr_title, discussions, repo_url):
    dependencies = tech_stack(repo_url)
    prompt = f"""
You are a experienced open source developer and maintainer and are tasked with assigning story points to the task to be done.
For the task: {pr_title} evaluate the story points needed to solve it based on the discussions and technial details of the repo given below.

Discussions:
{discussions}

Technical Dependencies:
{dependencies}

Output only an integer in form of story points.
"""
    response = call_llm(prompt)
    return response
