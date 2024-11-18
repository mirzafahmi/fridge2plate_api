from dotenv import load_dotenv
import os
import uuid

from db.db_setup import get_db
from utils.uom import post_uom
from pydantic_schemas.uom import UOMCreateSeeder


uoms = [
    {
        'id': '90b1d5ef-e50c-4e04-b321-24a28523f913',
        'name': 'kilogram',
        'unit': 'kg',
        'weightage': 1000
    },
    {
        'id': '8b4d558a-ad3e-4e06-b14b-3cbf89f861df',
        'name': 'gram',
        'unit': 'g',
        'weightage': 1
    },
    {
        'id': 'd50a071c-944a-4492-8e68-d2a61523e179',
        'name': 'clove',
        'unit': 'clove',
        'weightage': 1
    },
    {
        'id': '7b3a717b-a011-41e9-a818-348e92140b3a',
        'name': 'piece',
        'unit': 'piece',
        'weightage': 1
    },
    {
        'id': 'f3031b1f-581d-4304-8c26-0fc6ff9a7e66',
        'name': 'tablespoon',
        'unit': 'tbsp',
        'weightage': 3
    },
    {
        'id': '3f4ea71a-f8a3-4d8f-8a52-41dcea1cf6b5',
        'name': 'teaspoon',
        'unit': 'tsp',
        'weightage': 1
    },
    {
        'id': '590194af-95ee-43fb-9b77-abc52cdb26f6',
        'name': 'pinch',
        'unit': 'pinch',
        'weightage': 1
    },
    {
        'id': '3fc0e23d-0f9a-4a80-901a-dd94dc14bfbd',
        'name': 'slice',
        'unit': 'slice',
        'weightage': 1
    },
]

def seed_uom_data():
    db = next(get_db())

    for uom in uoms:
        try:
            uom_data = UOMCreateSeeder(**uom)
            created_uom = post_uom(db, uom_data )

            print(f'UOM data of {created_uom.name} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
    db.close()

    print('Seeding process for uom db is completed')

if __name__ == "__main__":
    seed_uom_data()