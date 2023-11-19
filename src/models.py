from sqlalchemy import Column, Integer, String

from .database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    md5_hash = Column(String)
