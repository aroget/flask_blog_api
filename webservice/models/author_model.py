from webservice import db

from webservice.models.user_model import User
from webservice.models.base_model import Base

class Author(Base):
    __tablename__ = "authors"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='author')
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Author %r>' % self.id