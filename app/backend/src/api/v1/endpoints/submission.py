from fastapi import APIRouter

from instances import classifier
from schemas import SubmissionRequest, SubmissionResponse

router = APIRouter()


@router.post("/", response_model=SubmissionResponse)
async def handle_submission(request: SubmissionRequest):
    try:
        result = classifier.predict(text=request.content)
        return {"content": result[0]}
    except Exception as ex:
        return {"content": "Что-то пошло не так :("}
