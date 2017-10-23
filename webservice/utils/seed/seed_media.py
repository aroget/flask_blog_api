import time
import random
from faker import Faker

from webservice import db
from webservice.models.media_model import Media
from webservice.models.author_model import Author

fake = Faker()

def seed_media(max_count=500):
    authors = [author.id for author in Author.query.all() if author.user.is_active is True]

    for item in range(0, max_count):
        name = fake.sentence()
        media_type = 'image'
        is_active = random.random() > 0.5
        url = ('https://source.unsplash.com/random/700x700?image={}').format(time.time())
        author_id = random.choice(authors)

        media = Media(name=name, media_type=media_type,
                      url=url, author_id=author_id)

        media.is_active = is_active

        db.session.add(media)
        db.session.commit()

        print('new media added')


