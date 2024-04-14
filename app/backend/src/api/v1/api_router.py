from fastapi import APIRouter

from .endpoints import busness_logic, db_request, query, submission  # noqa

api_router = APIRouter()

api_router.include_router(query.router, prefix="/query", tags=["Query"])
api_router.include_router(submission.router, prefix="/submission", tags=["Submission"])
api_router.include_router(
    busness_logic.router, prefix="/request", tags=["Business logic"]
)
api_router.include_router(db_request.router, prefix="/db_request", tags=["DB Request"])
