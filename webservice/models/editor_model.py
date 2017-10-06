from webservice import db

from webservice.models.user_model import User
from webservice.models.base_model import Base

class Editor(Base):
    __tablename__ = "editors"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='editor')

    def __repr__(self):
        return '<Editor %r>' % self.id