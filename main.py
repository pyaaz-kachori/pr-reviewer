from fastapi import FastAPI
from pydantic import BaseModel
from types.types import PRModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/pr")
async def check_pr(pr: PRModel):
    print(pr)
    pass