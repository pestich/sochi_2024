from core.config import settings
from db.session import engine
from instances import s3
from models.base_class import Base


# Create tables
async def init_models() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def init_s3() -> None:
    try:
        s3.create_bucket(Bucket=settings.MINIO_BUCKET)
    except:
        pass


async def init_db() -> None:
    await init_models()
    await init_s3()
