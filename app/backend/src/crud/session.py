from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Attempt, Session


async def check_or_create_session(session: AsyncSession, session_id: str) -> None:
    result = await session.execute(select(Session).filter(Session.id == session_id))
    session_instance = result.scalars().first()

    if session_instance is None:
        session_instance = Session(id=session_id)
        session.add(session_instance)

    attempt_instance = Attempt(session_id=session_id)
    session.add(attempt_instance)
    await session.commit()

    return attempt_instance.id
