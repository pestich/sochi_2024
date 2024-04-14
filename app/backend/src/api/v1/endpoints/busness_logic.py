import io
from typing import Any, List  # noqa

from fastapi import (APIRouter, Body, Depends, File, Form, Response, Security,
                     UploadFile, status)
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from unstructured.partition.auto import partition

import crud
from core.config import settings
from db.session import async_session
from instances import classifier, s3

router = APIRouter()


@router.post(
    "/",
)  # response_model=...
async def handle_request(
    files: List[UploadFile] = File(...), session_id: str = Form(...)
):
    predict_list = []
    async with async_session() as session:
        attempt_id = await crud.check_or_create_session(session, session_id)

        texts = []
        for file in files:
            contents = await file.read()
            bytes_io = io.BytesIO(contents)

            elements = partition(
                file=bytes_io, file_filename=file.filename, strategy="fast"
            )
            res = "\n\n".join([str(el) for el in elements])
            texts.append(res)

            predict = classifier.predict(text=res)[0]
            predict_list.append(predict)

            minio_file_id = f"{session_id}_{file.filename}"
            bucket = s3.Bucket(settings.MINIO_BUCKET)
            bucket.upload_fileobj(bytes_io, minio_file_id)

            file_data = {
                "name": file.filename,
                "content": res,
                "minio_id": minio_file_id,
                "attempt_id": attempt_id,
                "category": predict,
            }
            _ = await crud.create_file_entry(session, file_data)

            await file.close()

        response = classifier.validate_docs(predict_list)
        if response[0] == "Документы прошли валидацию и успешно загружены!":
            await crud.update_attempt_status(session, attempt_id, new_status=True)
        return response
