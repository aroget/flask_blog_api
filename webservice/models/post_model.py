import time

from webservice import db
from webservice.models.base_model import Base
from webservice.models import author_model, tag_model, media_model

class Post(Base):
    __tablename__ = "posts"

    is_private = db.Column(db.Boolean, default=False)
    is_draft = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    published_date = db.Column(db.Integer)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    likes = db.Column(db.Integer)
    feature_image = db.Column(db.Integer, db.ForeignKey('media.id'), default=None)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    draft = db.relationship('Draft', uselist=False, back_populates='post')

    def __init__(self, is_private, is_draft, is_published,
                 published_date, updated_on, title, body,
                 likes, feature_image):
        self.is_private = is_private
        self.is_draft = is_draft
        self.is_published = is_published
        self.published_date = published_date
        self.updated_on = updated_on
        self.title = title
        self.body = body
        self.likes = likes
        self.feature_image = feature_image

    def __repr__(self):
        return '<Post %r>' % self.title