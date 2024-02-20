from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationDB,
    DonationCreate,
    DonationUser
)
from app.models import User
from app.core.user import current_user, current_superuser
from app.services.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперпользователей."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Только для зарегистрированных пользователей."""
    new_donation = await donation_crud.create(
        donation,
        session,
        user,
    )
    investing(
        new_donation,
        await charity_project_crud.get_all_not_invested(session)
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUser]
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех пожертвований текущего пользователя."""
    return await donation_crud.get_by_user(
        session=session, user=user
    )
