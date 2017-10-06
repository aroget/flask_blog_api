from webservice import db
from webservice.models.base_model import Base

class Invitation(Base):
    __tablename__ = "invitations"

    key = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Invitation %r>' % self.id

