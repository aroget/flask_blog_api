import time

from webservice import db
from webservice.models.base_model import Base
from webservice.models.tag_model import Tag
from webservice.models.media_model import Media
from webservice.models.likes_model import likes

class Post(Base):
    __tablename__ = "posts"

    is_private = db.Column(db.Boolean, default=False)
    is_draft = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    published_date = db.Column(db.DateTime)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    likes = db.relationship('User', secondary=likes, lazy='subquery',
        backref=db.backref('posts', lazy=True))
    feature_image = db.Column(db.Integer, db.ForeignKey('media.id'), default=None)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    draft = db.relationship('Draft', uselist=False, back_populates='post')

    def __init__(self, title, body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id

    def is_author(self, author_id):
        return self.author_id == author_id

    def __repr__(self):
        return '<Post %r>' % self.title

    @property
    def serialize(self):
        tag = None
        media = None

        if self.tag_id:
            tag = Tag.query.get(self.tag_id)

            if tag is not None and tag.is_active:
                tag = tag.serialize

        if self.feature_image:
            media = Media.query.get(self.feature_image)

            if media is not None and media.is_active:
                media = media.serialize

        return {
            "id": self.id,
            "is_private": self.is_private,
            "is_draft": self.is_draft,
            "is_published": self.is_published,
            "published_date": self.published_date,
            "title": self.title,
            "body": self.body,
            "tag": tag,
            "likes": len(self.likes),
            "feature_image": media
        }