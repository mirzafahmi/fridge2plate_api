import random

from db.db_setup import get_db
from utils.follower import toggle_follow
from utils.user import get_user


NUM_FOLLOWS = 20 

def seed_follow_data():
    db = next(get_db())

    users = get_user(db)
    user_ids = [user.id for user in users]

    follow_pairs = set() 

    for _ in range(NUM_FOLLOWS):
        following_id, follower_id = random.sample(user_ids, 2)
        
        if (following_id, follower_id) not in follow_pairs:
            follow_pairs.add((following_id, follower_id))

            try:
                follow_entry = toggle_follow(db, follower_id, following_id)

                print(f'follow data of {follower_id} followed by {following_id} has been added to the database.')
        
            except Exception as e:
                db.rollback()
                print(f'Seeding process failed: {e}')
                continue
    
    db.close()

    print(f'Seeded {len(follow_pairs)} follow relationships!')

if __name__ == "__main__":
    seed_follow_data()