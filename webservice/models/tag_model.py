from webservice import db
from sqlalchemy import UniqueConstraint

from webservice.models import user_model
from webservice.models.base_model import Base

class Tag(Base):
    __tablename__ = "tags"

    label = db.Column(db.String(80))
    is_active = db.Column(db.Boolean, default=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    __table_args__ = (
        db.UniqueConstraint(label, author_id),
    )

    def __init__(self, label, author_id):
        self.label = label
        self.author_id = author_id

    def __repr__(self):
        return '<Label %r>' % self.label

    def is_from_author(self, author_id):
        return self.author_id == author_id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'author_id': self.author_id,
            'is_active': self.is_active,
        }
