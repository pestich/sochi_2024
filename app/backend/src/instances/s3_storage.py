import boto3

from core.config import settings

s3 = boto3.resource(
    "s3",
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_LOGIN,
    aws_secret_access_key=settings.MINIO_PASS,
)
