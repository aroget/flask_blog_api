from webservice import db

from webservice.models.base_model import Base

class Media(Base):
    __tablename__ = "media"

    name = db.Column(db.String(120))
    url = db.Column(db.String(200))
    media_type = db.Column(db.String(80))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __init__(self, name, url, media_type):
        self.url = url
        self.name = name
        self.media_type = media_type

    def __repr__(self):
        return '<Media %r>' % self.label