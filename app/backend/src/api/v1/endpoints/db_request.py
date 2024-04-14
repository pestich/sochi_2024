import io
import mimetypes
import os
import shutil
import zipfile
from typing import Any, Dict, List  # noqa
from urllib.parse import quote

from fastapi import (APIRouter, Body, Depends, File, Form, Response, Security,
                     UploadFile, status)
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from unstructured.partition.auto import partition

import crud
from core.config import settings
from db.session import async_session
from instances import classifier, s3

router = APIRouter()


@router.get(
    "/session",
)  # response_model=...
async def handle_request(session_id):
    async with async_session() as session:
        result = await crud.get_attempts_by_session_id(session, session_id)
        return result


@router.get(
    "/files",
)  # response_model=...
async def handle_request(attempt_id):
    async with async_session() as session:
        result = await crud.get_files_by_attempt_id(session, int(attempt_id))
        return result


@router.post("/download/")
async def create_upload_file(request: List[str]):
    # data = await request.json()  # Assuming JSON input containing the list of filenames
    file_names = request  # A list of filenames to be downloaded
    base_dir = os.getcwd()

    # Формирование абсолютного пути к директории temp_downloads
    temp_downloads_path = os.path.join(base_dir, "temp")
    try:
        shutil.rmtree(temp_downloads_path)
    except Exception as ex:
        print(ex)

    # Проверка на существование пути, и создание если он не существует
    if not os.path.exists(temp_downloads_path):
        os.makedirs(temp_downloads_path, exist_ok=True)
    try:
        # Download each file and save it locally
        for file_name in file_names:
            local_path = os.path.join(temp_downloads_path, file_name)
            with open(local_path, "wb") as f:
                obj = s3.Object(bucket_name=settings.MINIO_BUCKET, key=file_name)
                response = obj.get()
                print(local_path)
                file_content = response["Body"].read()
                f.write(file_content)

            # with open(local_path, 'wb') as f:
            #     s3.download_fileobj(Bucket=settings.MINIO_BUCKET, Key=file_name, Fileobj=f)

        # Create a zip archive of the downloaded files
        zip_path = os.path.join(temp_downloads_path, "downloaded_files.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file_name in file_names:
                print("ЗАПИСАЛИ!")
                print(file_name)
                t_path = os.path.join(temp_downloads_path, file_name)
                print(t_path)
                zipf.write(t_path, arcname=file_name)
        print(zip_path)
        return FileResponse(
            zip_path, media_type="application/zip", filename="downloaded_files.zip"
        )
    except Exception as ex:
        print(ex)
