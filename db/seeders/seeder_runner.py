from db.seeders.user_seeder import seed_user_data
from db.seeders.uom_seeder import seed_uom_data
from db.seeders.ingredient_category_seeder import seed_ingredient_category_data
from db.seeders.ingredient_seeder import seed_ingredient_data
from db.seeders.recipe_category_seeder import seed_recipe_category_data
from db.seeders.recipe_origin_seeder import seed_recipe_origin_data
from db.seeders.recipe_tag_seeder import seed_recipe_tag_data
from db.seeders.recipe_seeder import seed_recipe_data

def run_seeder():
    seed_user_data()
    seed_uom_data()
    seed_ingredient_category_data()
    seed_ingredient_data()
    seed_recipe_category_data()
    seed_recipe_origin_data()
    seed_recipe_tag_data()
    seed_recipe_data()

def run_deseeder():
    pass

if __name__ == "__main__":
    run_seeder()