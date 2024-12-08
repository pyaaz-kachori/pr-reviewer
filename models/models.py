from pydantic import BaseModel
from typing import List

class Patch(BaseModel):
    filename: str
    raw_url: str
    patch: str

class Comment(BaseModel):
    username: str
    body: str

class Commit(BaseModel):
    username: str
    message: str
    
class PRModel(BaseModel):
    url: str
    title: str
    contributor: str
    discussions: List[Comment]
    changes: List[Patch]
    # commits: List[Commit] | None

class Response(BaseModel):
    url: str
    review_score: int
    username: str
    explanation: str