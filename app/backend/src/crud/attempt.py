from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Attempt


async def update_attempt_status(
    session: AsyncSession, attempt_id: int, new_status: bool
) -> None:
    await session.execute(
        update(Attempt).where(Attempt.id == attempt_id).values(status=new_status)
    )
    await session.commit()


async def get_attempts_by_session_id(session: AsyncSession, session_id: str):
    result = await session.execute(
        select(Attempt).where(Attempt.session_id == session_id)
    )
    attempts = result.scalars().all()
    return attempts
