from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime

from app.core.db import Base


class CharityProject(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    close_date = Column(DateTime)

    def __repr__(self):
        return super().__repr__() + f', {self.name}, {self.description}'