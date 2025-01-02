import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean, Text, Float, Table
from sqlalchemy.dialects.postgresql import UUID
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

from ..db_setup import Base
from .timestamp_mixin import TimestampMixin
#from .recipe import Recipe, RecipeTagRecipeAssociation


load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")

class User(TimestampMixin, Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    providers = relationship("UserProvider", back_populates="user")

    
    ingredient_categories = relationship("IngredientCategory", back_populates="creator")
    ingredients = relationship("Ingredient", back_populates="creator")
    uoms = relationship("UOM", back_populates="creator")
    recipe_categories = relationship("RecipeCategory", back_populates="creator")
    recipe_origins = relationship("RecipeOrigin", back_populates="creator")
    recipe_tags = relationship("RecipeTag", back_populates="creator")
    recipes = relationship("Recipe", back_populates="creator")
    badges = relationship("Badge", back_populates="creator")

    user_badge_associations = relationship(
        "UserBadgeAssociation", 
        back_populates="user", 
        cascade="all, delete"
    )


    def set_email(self, email):
        try:
            valid_email = validate_email(email)
            self.email = valid_email['email']  # store the normalized form
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {e}")

class UserProvider(TimestampMixin, Base):
    __tablename__ = 'user_providers'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    provider = Column(String)
    provider_id = Column(String)
    provider_token = Column(String)
    provider_refresh_token = Column(String)

    user = relationship("User", back_populates="providers")

class Badge(TimestampMixin, Base):
    __tablename__ = 'badges'
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String, unique=True)
    description = description = Column(Text, nullable=True)
    image = Column(Text, nullable=False)

    user_badge_associations = relationship("UserBadgeAssociation", back_populates="badge")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="badges")

class UserBadgeAssociation(TimestampMixin, Base):
    __tablename__ = 'user_badge_associations'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="user_badge_associations")

    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=False)
    badge = relationship("Badge", back_populates="user_badge_associations")
