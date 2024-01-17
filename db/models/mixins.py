from datetime import datetime

from sqlalchemy import Column, DateTime, func 
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class UtilsField:
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
