import uuid
from .extensions import db


def gen_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    email = db.Column(db.String(320), index=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
