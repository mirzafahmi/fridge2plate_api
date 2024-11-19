from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import user, ingredient_category, ingredient, uom, recipe_category, recipe_tag, recipe_origin, recipe,ingredient_recipe_association


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Include routers
app.include_router(user.router)
app.include_router(ingredient_category.router)
app.include_router(ingredient.router)
app.include_router(uom.router)
app.include_router(recipe_category.router)
app.include_router(recipe_tag.router)
app.include_router(recipe_origin.router)
app.include_router(recipe.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(ingredient_recipe_association.router)

@app.router.get("/", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def server_check():
    return "Fridge2plate API server is running"