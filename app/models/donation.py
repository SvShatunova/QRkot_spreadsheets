from sqlalchemy import Column, ForeignKey, Text, Integer

from app.models.base import CharityBase


class Donation(CharityBase):
    """Модель для пожертвований."""
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
