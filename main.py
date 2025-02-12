from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference
from api import user, badge, ingredient_category, ingredient, uom, recipe_category, recipe_tag, recipe_origin, recipe, ingredient_recipe_association, recipe_tag_recipe_association, recipe_instruction, recipe_image, recipe_tip, recipe_form


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
app.include_router(badge.router)
app.include_router(ingredient_category.router)
app.include_router(ingredient.router)
app.include_router(uom.router)
app.include_router(recipe_category.router)
app.include_router(recipe_origin.router)
app.include_router(recipe_tag.router)
app.include_router(recipe.router)
app.include_router(ingredient_recipe_association.router)
app.include_router(recipe_tag_recipe_association.router)
app.include_router(recipe_instruction.router)
app.include_router(recipe_image.router)
app.include_router(recipe_tip.router)
app.include_router(recipe_form.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.router.get("/", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def server_check():
    return "Fridge2plate API server is running"

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title + " - Scalar",
    )