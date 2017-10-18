from .seed_users import seed_users
from .seed_authors import seed_authors
from .seed_tags import seed_tags

def seed():
    seed_users(500)
    seed_authors()
    seed_tags()

