from werkzeug.security import generate_password_hash, check_password_hash

from webservice import db
from webservice.models.base_model import Base
from webservice.models.likes_model import likes

class User(Base):
    __tablename__ = "users"

    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    user_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(200))
    avatar = db.Column(db.String(200), default=None)
    likes = db.relationship('Post', secondary=likes, lazy='subquery',
        backref=db.backref('users', lazy=True))
    is_active = db.Column(db.Boolean, default=False)
    is_disabled = db.Column(db.Boolean, default=False)
    author = db.relationship('Author', uselist=False, back_populates='user')
    editor = db.relationship('Editor', uselist=False, back_populates='user')

    @property
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "email": self.email,
            "avatar": self.avatar,
            "likes": [post.id for post in self.likes],
            "is_active": self.is_active,
            "is_disabled": self.is_disabled
        }

    def is_author(self):
        return self.author is not None

    def is_editor(self):
        return self.editor is not None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, first_name, last_name, user_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.email = email
        self.set_password(password)
        # self.avatar = avatar
        # self.likes = likes
        # self.is_active = is_active
        # self.is_disabled = is_disabled

    def __repr__(self):
        return '<User %r>' % self.user_name
