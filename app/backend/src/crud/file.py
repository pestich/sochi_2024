from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import File


async def create_file_entry(session: AsyncSession, file_data: dict) -> File:
    new_file = File(
        name=file_data["name"],
        content=file_data["content"],
        minio_id=file_data["minio_id"],
        attempt_id=file_data["attempt_id"],
        category=file_data["category"],
    )
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return new_file


async def get_files_by_attempt_id(session: AsyncSession, attempt_id: int) -> list[File]:
    query = select(File).where(File.attempt_id == attempt_id)
    result = await session.execute(query)
    files = result.scalars().all()
    return files
