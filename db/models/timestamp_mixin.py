from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class TimestampMixin:
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

