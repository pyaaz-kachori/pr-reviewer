from agents.quality.code_smells import code_smells_agent
from agents.quality.spams import spams_agent
from models.models import PRModel
from llm import call_llm
from pydantic import BaseModel
import json

class Quality(BaseModel):
    score: int
    explanation: str | None

def quality_eval(pr: PRModel):
    smells = code_smells_agent(pr.changes)
    spams = spams_agent(pr.changes)
    prompt = f"""
You are a code evaluator who is given a PR and scores the PR on a scale of 0 to 1000 with 1000 being highest possible score.
Initially the score stands at 1000 is reduced towards zero as code smells and spams increase along with their severity.

The changes in the PR are as follows:
{pr.changes}

The code smells, that is issues with the codes are as follows:
{smells.model_dump_json()}

Indicators of spam PR are as follows:
{spams.model_dump_json()}

Ensure that severity of smells and spams have a heavy impact on score deduction due to issues.

Give the output in form of json dump following the provided pydantic models
class Quality(BaseModel):
    score: int
    explanation: str | None

Do not provide any output other than json dump.
"""
    response = call_llm(prompt)
    try:
        return Quality(**json.loads(response[7:-3]))
    except:
        correction_prompt = f"""
From the following text find out final score, only output a single integer:
{response}
"""
        try:
            score = Quality(score=call_llm(correction_prompt), explanation="")
            return score
        except:
            print("Failed at evaluating score")
            return Quality(score=100, explanation="")