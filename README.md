# fridge2plate_api

## Table of Contents
- [How to Setup the API]

## How to Setup the API

1. run migration 
   ```
   alembic revision --autogenerate -m "init"
   alembic upgrade head
   ```

2. run seeder
   
    ```
        python -m db.seeders.seeder_runner
    ```

3. run test
   