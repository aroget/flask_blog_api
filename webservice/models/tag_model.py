from webservice import db

from webservice.models import user_model
from webservice.models.base_model import Base

class Tag(Base):
    __tablename__ = "tags"

    label = db.Column(db.String(80), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, label, user_id):
        self.label = label
        self.user_id = user_id

    def __repr__(self):
        return '<Label %r>' % self.label

    @property
    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'user_id': self.user_id,
            'is_active': self.is_active,
        }
