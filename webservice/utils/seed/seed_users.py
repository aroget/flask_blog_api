import time
import random
from faker import Faker

from webservice import db
from sqlalchemy.exc import IntegrityError
from webservice.models.user_model import User
fake = Faker('en_CA')

def seed_users(max_count=1000):
    for index in range(0, max_count):
        full_name = fake.name()
        first_name = full_name.split(' ')[0]
        last_name = full_name.split(' ')[1]
        user_name = (first_name[0] + last_name).lower()
        email = ("{}@gmail.com").format(first_name)

        user = User(first_name=first_name,
                    password="password",
                    last_name=last_name,
                    user_name=user_name,
                    email=email,
                    )

        avatar = "https://source.unsplash.com/random/130x130?id={}".format(time.time())
        user.avatar = avatar
        user.is_disabled = random.random() > 0.5

        if user.is_disabled is False:
            user.is_active = random.random() > 0.5

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            continue

        print(('{} created').format(user_name))
