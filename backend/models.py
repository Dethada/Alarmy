import uuid
from .extensions import db
from sqlalchemy_utils.types.choice import ChoiceType


def gen_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    ROLES = [
        (u'admin', u'Admin'),
        (u'user', u'User')
    ]

    __tablename__ = 'users'
    uuid = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    email = db.Column(db.String(320), index=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(ChoiceType(ROLES), default='user', nullable=False)
    password = db.Column(db.String(80), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'uuid': self.uuid,
            'email': self.email,
            'name': self.name,
            'role': self.role,
        }

    def __repr__(self):
        return '<User %r>' % self.email
