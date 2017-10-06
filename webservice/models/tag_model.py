from webservice import db

from webservice.models import user_model
from webservice.models.base_model import Base

class Tag(Base):
    __tablename__ = "tags"

    label = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return '<Label %r>' % self.label