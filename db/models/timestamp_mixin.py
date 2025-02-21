from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class TimestampMixin:
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def override_timestamps(cls, instances, created=None, updated=None):
        """For testing only: allows manual timestamp setting on an instance or a list of instances."""
        if not isinstance(instances, list):
            instances = [instances]  # Convert a single instance to a list

        for instance in instances:
            if created:
                instance.created_date = created
            if updated:
                instance.updated_date = updated
