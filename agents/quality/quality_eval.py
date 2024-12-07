from agents.quality.code_smells import code_smells_agent
from agents.quality.spams import spams_agent
from models.models import PRModel
from llm import call_llm

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
Output only an integer, it being the score out of 1000. Dont output any additional text.
"""
    response = call_llm(prompt)
    try:
        return int(response)
    except:
        correction_prompt = f"""
From the following text find out final score, only output a single integer:
{response}
"""
        try:
            score = int(call_llm(correction_prompt))
            return score
        except:
            print("Failed at evaluating score")
            return None