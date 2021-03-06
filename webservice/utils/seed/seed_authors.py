import random

from webservice import db
from webservice.models.user_model import User
from webservice.models.author_model import Author

user_ids = [user.id for user in User.query.all() if user.author is None]

def seed_authors():
    for index in user_ids:
        if index % 2:
            continue

        user_id = index
        is_active = random.random() > 0.5
        author = Author(user_id=user_id, is_active=is_active)

        db.session.add(author)
        db.session.commit()
        print(('{} created').format(user_id))
