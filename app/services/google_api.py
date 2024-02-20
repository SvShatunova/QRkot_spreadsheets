from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import (
    settings,
    DATE_FORMAT,
    ROW_COUNT,
    COLUMN_COUNT
)

SPREADSHEET_BODY = {
    'properties': {
        'title': '',
        'locale': 'ru_RU'
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': ROW_COUNT,
                    'columnCount': COLUMN_COUNT
                }
            }
        }
    ]
}

TABLE_VAIUES = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
InvalidTableLength = 'Превышено допустимое количество строк/столбцов в таблице.'


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=SPREADSHEET_BODY
) -> tuple[str, str]:
    """Создание гугл-таблицы."""
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(spreadsheet_body)
    spreadsheet_body['properties']['title'] = (
        f'Отчёт от {datetime.now().strftime(DATE_FORMAT)}'
    )

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheet_Id'], response['spreadsheet_url']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Выдача прав личному аккаунту."""
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    table_data = [
        [project.name,
         str(project.close_date - project.create_date),
         project.description]
        for project in charity_projects
    ]
    table_data = sorted(table_data, key=lambda x: x[1])
    service = await wrapper_services.discover('sheets', 'v4')
    table_head = deepcopy(TABLE_VAIUES)
    table_head[0][1] = datetime.now().strftime(DATE_FORMAT)
    table_values = {
        *table_head,
        *table_data
    }
    row_length = len(table_values)
    column_length = max(map(len, table_values))
    if row_length > ROW_COUNT or column_length > COLUMN_COUNT:
        raise InvalidTableLength(
            'Превышено допустимое количество строк/столбцов в таблице.'
            f'Количество строк: {row_length}. '
            f'Допустимое количество строк: {ROW_COUNT}.'
            f'Количество столбцов: {row_length}.'
            f'Допустимое количество столбцов: {ROW_COUNT}.'
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': TABLE_VAIUES
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{row_length}C{column_length}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
