import io
import mimetypes
import os
import shutil
import tempfile
import zipfile
from typing import Any, List  # noqa
from urllib.parse import quote
from zipfile import ZipFile

import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import (APIRouter, Body, Depends, File, Form, HTTPException,
                     Response, Security, UploadFile, status)
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from unstructured.partition.auto import partition

import crud  # noqa
import models
import schemas
from core.config import settings
from db.session import async_session
from instances import classifier, s3

router = APIRouter()


@router.post("/upload/single_doc")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        bytes_io = io.BytesIO(contents)
        elements = partition(
            file=bytes_io, file_filename=file.filename, strategy="fast"
        )
        res = "\n\n".join([str(el) for el in elements])
        await file.close()

        return res
    except Exception as ex:
        return "Что-то пошло не так :("


@router.post("/upload/single_doc/classify")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    bytes_io = io.BytesIO(contents)
    elements = partition(file=bytes_io, file_filename=file.filename, strategy="fast")
    res = "\n\n".join([str(el) for el in elements])
    await file.close()
    try:
        result = classifier.predict(res)
        return {"content": result[0]}
    except Exception as ex:
        return {"content": "Что-то пошло не так :("}
