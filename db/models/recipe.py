from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean, Text, Float, Table
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import UtilsField


class IngredientCategory(UtilsField, Base):
    __tablename__ = "ingredient_category"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    ingredient = relationship("Ingredient", back_populates="ingredient_category")


class Ingredient(UtilsField, Base):
    __tablename__ = "ingredient"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    brand = Column(String(100), index=True, nullable=False)
    is_essential = Column(Boolean, default=False)
    icon = Column(Text, nullable=True)

    ingredient_category_id = Column(Integer, ForeignKey("ingredient_category.id"), nullable=False)
    ingredient_category = relationship("IngredientCategory", back_populates="ingredient")

    recipe = relationship("Recipe", secondary="ingredient_recipe_association", back_populates="ingredients")
    


class UOM(UtilsField, Base):
    __tablename__ = "uom"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    unit = Column(String(10), unique=True, index=True, nullable=False)
    weightage = Column(Float)



class RecipeCategory(UtilsField, Base):
    __tablename__ = "recipe_category"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    recipe = relationship("Recipe", back_populates="recipe_category")


class RecipeTag(UtilsField, Base):
    __tablename__ = "recipe_tag"
        
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    recipe = relationship("Recipe", back_populates="recipe_tag")


class RecipeOrigin(UtilsField, Base):
    __tablename__ = "recipe_origin"
        
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    recipe = relationship("Recipe", back_populates="recipe_origin")


# ingredient_recipe_association = Table(
#     'ingredient_recipe',
#     Base.metadata,
#     Column('recipe_id', Integer, ForeignKey('recipe.id')),
#     Column('ingredient_id', Integer, ForeignKey('ingredient.id')),
#     Column('quantity', Integer),
#     Column('uom_id', Integer, ForeignKey('uom.id'))
# )


class IngredientRecipeAssociation(Base):
    __tablename__ = "ingredient_recipe_association"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    ingredient = relationship("Ingredient", overlaps="recipe")
    recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
    quantity = Column(Integer)
    uom_id = Column(Integer, ForeignKey("uom.id"))
    uom = relationship("UOM")


class Recipe(UtilsField, Base):
    __tablename__ = "recipe"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    serving = Column(Integer, index=True, nullable=True)
    cooking_time = Column(String(100), index=True, nullable=False)
    author = Column(String(100), index=True, nullable=False)
    instructions = Column(Text, index=True, nullable=True)


    recipe_category_id = Column(Integer, ForeignKey("recipe_category.id"), nullable=True)
    recipe_category = relationship("RecipeCategory", back_populates="recipe")

    recipe_tag_id = Column(Integer, ForeignKey("recipe_tag.id"), nullable=True)
    recipe_tag = relationship("RecipeTag", back_populates="recipe")

    recipe_origin_id = Column(Integer, ForeignKey("recipe_origin.id"), nullable=True)
    recipe_origin = relationship("RecipeOrigin", back_populates="recipe")
    
    
    ingredients = relationship("Ingredient", secondary="ingredient_recipe_association", back_populates="recipe", overlaps="ingredient")
    ingredients_recipe_associations = relationship("IngredientRecipeAssociation", overlaps="ingredients,recipe")