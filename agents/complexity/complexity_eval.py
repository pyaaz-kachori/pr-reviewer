from llm import call_llm
from agents.complexity.tech_stack import tech_stack
from pydantic import BaseModel
import json
from models.models import PRModel

class Complexity(BaseModel):
    story_points: int
    explanation: str | None

def complexity_eval(pr: PRModel):
    dependencies = tech_stack(pr.url)
    prompt = f"""
You are a experienced open source developer and maintainer and are tasked with assigning story points to the task to be done.
For the task: {pr.title} evaluate the story points needed to solve it based on the discussions and technial details of the repo given below.

Discussions:
{pr.discussions}

Technical Dependencies:
{dependencies}

Give the output in form of json dump following the provided pydantic models
class Complexity(BaseModel):
    story_points: int
    explanation: str | None

Do not provide any output other than json dump.
"""
    response = call_llm(prompt)
    try:
        fin = Complexity(**json.loads(response[7:-3]))
        return fin
    except:
        print(f"Failed at complexity agent")
        return Complexity(story_points=1, explanation="")
