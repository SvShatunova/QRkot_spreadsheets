from datetime import datetime

from typing import List

from app.models.base import CharityBase


def investing(
        target: CharityBase,
        sources: List[CharityBase],
) -> List[CharityBase]:
    """Полный процесс инвестирования с сохранением данных в БД."""
    updated = []

    for source in sources:
        available_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for investment in [target, source]:
            investment.invested_amount += available_amount
            investment.fully_invested = (
                investment.invested_amount == investment.full_amount
            )
            if investment.fully_invested:
                investment.close_date = datetime.utcnow()
        updated.append(source)
        if target.fully_invested:
            break
    return updated
