from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationDB,
    DonationCreate,
    DonationUser
)
from app.models import User, CharityProject
from app.core.user import current_user, current_superuser
from app.services.investing import investing

router = APIRouter()


@router.get('/', response_model=list[DonationDB],
            dependencies=[Depends(current_superuser)],)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперпользователей."""
    return await donation_crud.get_multi(session)


@router.post('/', response_model=DonationUser,
             response_model_exclude_none=True,)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Только для зарегистрированных пользователей."""
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await investing(new_donation, CharityProject, session)
    return new_donation


@router.get('/my',
            response_model=list[DonationUser])
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех пожертвований текущего пользователя."""
    return await donation_crud.get_by_user(
        session=session, user=user
    )
