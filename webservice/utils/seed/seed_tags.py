import random

from webservice import db
from sqlalchemy.exc import IntegrityError
from webservice.models.tag_model import Tag
from webservice.models.author_model import Author

authors = Author.query.all();
author_ids = [author.id for author in authors]

dummy_tags = [ 'python','journalism','music',
               'camping','climbing','cycling',
               'sports','wine','food',
               'design','art','travel','books' ]


def seed_tags():
    for index in range(0, len(dummy_tags)):
        label = dummy_tags[index]
        author_id = random.choice(author_ids)

        tag = Tag(label=label,
                  author_id=author_id,
                )
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            continue
        print(('{} created').format(label))
