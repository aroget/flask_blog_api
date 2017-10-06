import time
from webservice import db

from webservice.models.user_model import User
from webservice.models.base_model import Base

class AccessToken(Base):
    __tablename__ = "access_tokens"

    token = db.Column(db.String(300))
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<AccessToken %r>' % self.id