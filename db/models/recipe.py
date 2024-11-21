import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

from ..db_setup import Base
from .timestamp_mixin import TimestampMixin
from db.models.user import User


load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")

class IngredientCategory(TimestampMixin, Base):
    __tablename__ = "ingredient_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)

    ingredients = relationship("Ingredient", back_populates="ingredient_category")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="ingredient_categories")


class Ingredient(TimestampMixin, Base):
    __tablename__ = "ingredients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)
    brand = Column(String(100), nullable=False)
    icon = Column(Text, nullable=True)

    ingredient_category_id = Column(UUID(as_uuid=True), ForeignKey("ingredient_categories.id"), nullable=True)
    ingredient_category = relationship("IngredientCategory", back_populates="ingredients")

    recipe = relationship("Recipe", secondary="ingredient_recipe_associations", back_populates="ingredients", overlaps="ingredient")
    
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="ingredients")


class UOM(TimestampMixin, Base):
    __tablename__ = "uoms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)
    unit = Column(String(10), unique=True, nullable=False)
    weightage = Column(Float)

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="uoms")


class RecipeCategory(TimestampMixin, Base):
    __tablename__ = "recipe_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="recipe_category")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="recipe_categories")


class RecipeTag(TimestampMixin, Base):
    __tablename__ = "recipe_tags"
        
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="recipe_tag")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="recipe_tags")


class RecipeOrigin(TimestampMixin, Base):
    __tablename__ = "recipe_origins"
        
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="recipe_origin")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="recipe_origins")


class IngredientRecipeAssociation(TimestampMixin, Base):
    __tablename__ = "ingredient_recipe_associations"

    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"), primary_key=True)
    ingredient = relationship("Ingredient", overlaps="recipe")

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), primary_key=True)
    recipe = relationship("Recipe", overlaps="ingredient,recipe")

    uom_id = Column(UUID(as_uuid=True), ForeignKey("uoms.id"), nullable=True)
    uom = relationship("UOM")

    quantity = Column(Integer, default=1)
    is_essential = Column(Boolean, default=False)

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="ingredient_recipe_associations")


class Recipe(TimestampMixin, Base):
    __tablename__ = "recipes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(Text, unique=True, nullable=False)
    serving = Column(Integer, nullable=True)
    cooking_time = Column(Text, nullable=False)
    instructions = Column(Text, nullable=True)


    recipe_category_id = Column(UUID(as_uuid=True), ForeignKey("recipe_categories.id"), nullable=True)
    recipe_category = relationship("RecipeCategory", back_populates="recipes")

    recipe_tag_id = Column(UUID(as_uuid=True), ForeignKey("recipe_tags.id"), nullable=True)
    recipe_tag = relationship("RecipeTag", back_populates="recipes")

    recipe_origin_id = Column(UUID(as_uuid=True), ForeignKey("recipe_origins.id"), nullable=True)
    recipe_origin = relationship("RecipeOrigin", back_populates="recipes")
    
    
    ingredients = relationship("Ingredient", secondary="ingredient_recipe_associations", back_populates="recipe", overlaps="ingredient,recipe")
    ingredient_recipe_associations = relationship("IngredientRecipeAssociation", overlaps="ingredients,recipe")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="recipes")