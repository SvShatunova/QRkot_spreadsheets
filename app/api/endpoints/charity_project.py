from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.core.db import get_async_session
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.crud.charity_project import charity_project_crud
from app.api.validators import (check_charity_project_exists,
                                check_name_duplicate,
                                check_charity_project_closed,
                                check_charity_project_invested_sum,
                                check_charity_project_already_invested)
from app.core.user import current_superuser
from app.services.investing import investing


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперпользователей."""
    await check_name_duplicate(
        charity_project.name,
        session
    )
    new_project = await charity_project_crud.create(
        charity_project,
        session,
    )
    session.add_all(
        investing(
            new_project,
            await donation_crud.get_all_not_invested(session)
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(
        session
    )
    return all_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    check_charity_project_already_invested(charity_project)
    check_charity_project_closed(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    check_charity_project_closed(charity_project)

    if obj_in.full_amount is not None:
        check_charity_project_invested_sum(charity_project, obj_in.full_amount)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )

    return charity_project
