from fastapi import FastAPI
from models.models import PRModel, Response

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from agents.complexity.complexity_eval import complexity_eval
from agents.quality.quality_eval import quality_eval

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/pr")
async def check_pr(pr: PRModel):
    # Score = semantics + 1000 - code smells wale negaives * complexity
    complexity = complexity_eval(pr).story_points
    quality = quality_eval(pr)
    response = Response(url=pr.url, review_score=complexity*quality, username=pr.contributor)
    print(response.model_dump_json())
    return response.model_dump_json()