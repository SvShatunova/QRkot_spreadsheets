from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


async def investing(session: AsyncSession):
    """Полный процесс инвестирования с сохранением данных в БД."""
    projects = await charity_project_crud.get_not_full_invested_objects(
        session)
    donations = await donation_crud.get_not_full_invested_objects(session)

    for project in projects:
        for donation in donations:
            if not project.fully_invested:
                min_amount = min(
                    project.full_amount - project.invested_amount,
                    donation.full_amount - donation.invested_amount)
                project.invested_amount += min_amount
                donation.invested_amount += min_amount
                if project.full_amount == project.invested_amount:
                    project.fully_invested = True
                    project.close_date = datetime.utcnow()
                if donation.full_amount == donation.invested_amount:
                    donation.fully_invested = True
                    donation.close_date = datetime.utcnow()

    await session.commit()
