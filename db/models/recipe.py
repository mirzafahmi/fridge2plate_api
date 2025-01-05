import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
import os
from dotenv import load_dotenv

from ..db_setup import Base
from .timestamp_mixin import TimestampMixin
#from db.models.user import User


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

    ingredient_category_id = Column(UUID(as_uuid=True), ForeignKey("ingredient_categories.id"), nullable=True)
    ingredient_category = relationship("IngredientCategory", back_populates="ingredients")

    recipes = relationship("Recipe", secondary="ingredient_recipe_associations", back_populates="ingredients", overlaps="ingredient_recipe_associations")
    
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="ingredients")

class UOM(TimestampMixin, Base):
    __tablename__ = "uoms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)
    unit = Column(String(10), unique=True, nullable=False)
    weightage = Column(Float, default=1)

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="uoms")

class RecipeCategory(TimestampMixin, Base):
    __tablename__ = "recipe_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="recipe_category")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="recipe_categories")

class RecipeOrigin(TimestampMixin, Base):
    __tablename__ = "recipe_origins"
        
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="recipe_origin")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="recipe_origins")

class RecipeTag(TimestampMixin, Base):
    __tablename__ = "recipe_tags"
        
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    name = Column(String(100), unique=True, nullable=False)

    recipe_tag_recipe_associations = relationship(
        "RecipeTagRecipeAssociation",
        back_populates="recipe_tag",
        cascade="all, delete"
    )

    recipes = relationship("Recipe", secondary="recipe_tag_recipe_associations", back_populates="recipe_tags", overlaps="recipe_tag_recipe_associations,recipe_tag")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="recipe_tags")

class IngredientRecipeAssociation(TimestampMixin, Base):
    __tablename__ = "ingredient_recipe_associations"
    
    __mapper_args__ = {
        "confirm_deleted_rows": False  # This will suppress the warning
    }

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())

    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"))
    ingredient = relationship("Ingredient", overlaps="recipes")

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="ingredient_recipe_associations", overlaps="ingredient,recipes", single_parent=True)

    uom_id = Column(UUID(as_uuid=True), ForeignKey("uoms.id"), nullable=True)
    uom = relationship("UOM")

    quantity = Column(Float, default=1)
    is_essential = Column(Boolean, default=False)

class RecipeTagRecipeAssociation(TimestampMixin, Base):
    __tablename__ = "recipe_tag_recipe_associations"

    __mapper_args__ = {
        "confirm_deleted_rows": False  # This will suppress the warning
    }

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())

    recipe_tag_id = Column(UUID(as_uuid=True), ForeignKey("recipe_tags.id"))
    recipe_tag = relationship("RecipeTag", back_populates="recipe_tag_recipe_associations", overlaps="recipes")

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="recipe_tag_recipe_associations", overlaps="recipe_tags,recipes", single_parent=True)

class Recipe(TimestampMixin, Base):
    __tablename__ = "recipes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    original_recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), nullable=True)
    name = Column(Text, nullable=False)
    serving = Column(String, nullable=True)
    cooking_time = Column(Text, nullable=False)

    steps = relationship("RecipeInstruction", back_populates="recipe", cascade="all, delete")
    tips = relationship("RecipeTip", back_populates="recipe", cascade="all, delete")
    images = relationship("RecipeImage", back_populates="recipe", cascade="all, delete")

    recipe_category_id = Column(UUID(as_uuid=True), ForeignKey("recipe_categories.id"), nullable=True)
    recipe_category = relationship("RecipeCategory", back_populates="recipes")

    recipe_origin_id = Column(UUID(as_uuid=True), ForeignKey("recipe_origins.id"), nullable=True)
    recipe_origin = relationship("RecipeOrigin", back_populates="recipes")

    recipe_tags = relationship("RecipeTag", secondary="recipe_tag_recipe_associations", back_populates="recipes", overlaps="recipe_tag_recipe_associations,recipe_tag")
    recipe_tag_recipe_associations = relationship("RecipeTagRecipeAssociation", back_populates="recipe", cascade="all, delete", overlaps="recipe_tags,recipes")
    
    ingredients = relationship("Ingredient", secondary="ingredient_recipe_associations", back_populates="recipes", overlaps="ingredient,recipe")
    ingredient_recipe_associations = relationship("IngredientRecipeAssociation", back_populates="recipe", cascade="all, delete", overlaps="ingredients,recipe") #if any error with seeding

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    creator = relationship("User", back_populates="recipes")

    recipe_user_associations = relationship("RecipeUserAssociation", back_populates="recipe", cascade="all, delete")

    @property
    def ingredient_data(self):
        # This property method ensures that the Pydantic model sees `ingredient_data`
        return self.ingredient_recipe_associations

class RecipeImage(TimestampMixin, Base):
    __tablename__ = "recipe_images"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    image = Column(Text, nullable=False)

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), nullable=False)
    recipe = relationship("Recipe", back_populates="images")

class RecipeInstruction(TimestampMixin, Base):
    __tablename__ = "instructions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    step_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), nullable=False)
    recipe = relationship("Recipe", back_populates="steps")

class RecipeTip(TimestampMixin, Base):
    __tablename__ = "recipe_tips"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    description = Column(Text, nullable=False)

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), nullable=False)
    recipe = relationship("Recipe", back_populates="tips")

class RecipeUserAssociation(TimestampMixin, Base):
    __tablename__ = "recipe_user_associations"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid.uuid4())
    cooked = Column(Boolean, default=False)
    cooked_date = Column(DateTime, nullable=True)
    liked = Column(Boolean, default=False)
    liked_date = Column(DateTime, nullable=True)
    bookmarked = Column(Boolean, default=False)
    bookmarked_date = Column(DateTime, nullable=True)

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), nullable=False)
    recipe = relationship("Recipe", back_populates="recipe_user_associations")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, default=ADMIN_ID)
    user = relationship("User", back_populates="recipe_user_associations")

    @validates('cooked', 'liked', 'bookmarked')
    def update_dates(self, key, value):
        if value and key == 'cooked':
            self.cooked_date = func.now()
        elif value and key == 'liked':
            self.liked_date = func.now()
        elif value and key == 'bookmarked':
            self.bookmarked_date = func.now()
        return value