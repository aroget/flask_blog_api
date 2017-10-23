import random

from webservice import db
from webservice.models.user_model import User
from webservice.models.editor_model import Editor

user_ids = [user.id for user in User.query.all() if user.editor is None]

def seed_editors():
    for index in user_ids:
        if index % 2:
            continue

        user_id = index
        is_active = random.random() > 0.5
        editor = Editor(user_id=user_id, is_active=is_active)

        db.session.add(editor)
        db.session.commit()
        print(('{} created').format(user_id))
