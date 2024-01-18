from fastapi import FastAPI
from api import ingredient_category, ingredient, uom, recipe_category, recipe_tag, recipe_origin


app = FastAPI(
    title="Fridge2Plate API",
    description="API for the recipe app based on fridge",
    version="0.1.0",
    contact={
        "name": "Mirza Fahmi",
        "email": "gwen@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Include routers
app.include_router(ingredient_category.router)
app.include_router(ingredient.router)
app.include_router(uom.router)
app.include_router(recipe_category.router)
app.include_router(recipe_tag.router)
app.include_router(recipe_origin.router)