from pydantic import BaseModel


class SubmissionRequest(BaseModel):
    content: str


class SubmissionResponse(BaseModel):
    content: str
