from webservice import db
from sqlalchemy_utils.types.choice import ChoiceType

from webservice.models.base_model import Base

SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png']

class Media(Base):
    MEDIA_TYPES = [
        ('image', 'IMAGE'),
        ('video', 'VIDEO'),
    ]
    __tablename__ = "media"

    name = db.Column(db.String(120))
    url = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    is_active = db.Column(db.Boolean, default=True)
    media_type = db.Column(ChoiceType(MEDIA_TYPES))

    def __init__(self, name, url, media_type, author_id):
        self.url = url
        self.name = name
        self.author_id = author_id
        self.media_type = media_type

    def __repr__(self):
        return '<Media %r>' % self.label

    @staticmethod
    def supported(extension):
        if extension.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError('Extension not supported')

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "media_type": self.media_type.value
        }