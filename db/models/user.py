import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean, Text, Float, Table
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .timestamp_mixin import TimestampMixin

class User(TimestampMixin, Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    providers = relationship("UserProvider", back_populates="user")

    def set_email(self, email):
        try:
            valid_email = validate_email(email)
            self.email = valid_email['email']  # store the normalized form
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {e}")

class UserProvider(TimestampMixin, Base):
    __tablename__ = 'user_providers'

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    provider = Column(String)
    provider_id = Column(String)
    provider_token = Column(String)
    provider_refresh_token = Column(String)

    user = relationship("User", back_populates="providers")