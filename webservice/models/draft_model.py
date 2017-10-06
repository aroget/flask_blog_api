from webservice import db

from webservice.models.post_model import Post
from webservice.models.base_model import Base

class Draft(Base):
    __tablename__ = "drafts"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.relationship('Post', back_populates='draft')

    def __repr__(self):
        return '<Draft %r>' % self.id