from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.graph import classify_message

app = FastAPI(
    title="LangGraph Email Classifier",
    description="Classifies email text and creates reply drafts. It does not send email.",
    version="1.0.0",
)


class ClassifyRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=300)
    email_body: str = Field(min_length=1, max_length=12000)


class ClassifyResponse(BaseModel):
    subject: str
    category: str
    reason: str
    response: str
    reply_created: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify", response_model=ClassifyResponse)
def classify(request: ClassifyRequest):
    try:
        return classify_message(request.subject, request.email_body)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        # Avoid returning stack traces or provider details to the client.
        raise HTTPException(
            status_code=502,
            detail="Email classification failed. Check server logs and try again.",
        ) from exc
