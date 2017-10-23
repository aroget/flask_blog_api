import random
import datetime
from faker import Faker

from webservice import db
from webservice.models.tag_model import Tag
from webservice.models.post_model import Post
from webservice.models.media_model import Media
from webservice.models.author_model import Author

fake = Faker()

tag_ids = [tag.id for tag in Tag.query.all() if tag.is_active is True]

author_ids = [author.id for author in Author.query.all() if author.user.is_disabled is False]
media_ids = [media.id for media in Media.query.all() if media.is_active is True]

def seed_posts(max_count=500):
    for item in range(0, max_count):
        is_private = random.random() > 0.5
        is_draft = random.random() > 0.5

        if is_draft:
            is_published = False
        else:
            is_published = True

        title = fake.sentence()
        body = fake.text()
        tag_id = random.choice(tag_ids)
        feature_image = random.choice(media_ids)
        author_id = random.choice(author_ids)

        post = Post(is_private = is_private, is_draft = is_draft,
                    is_published = is_published, title = title,
                    body = body, feature_image = feature_image)

        if is_published:
            # post.published_date = time.mktime(datetime.datetime.now().timetuple()) * 1000
            post.published_date = datetime.datetime.now()

        post.author_id = author_id
        post.tag_id = tag_id

        db.session.add(post)
        db.session.commit()

        print('new post!')


# from webservice.utils.seed.seed_posts import seed_posts

