from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    boards = db.relationship('Board', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    left_name = db.Column(db.String(30), nullable=False)
    right_name = db.Column(db.String(30), nullable=False)
    left_vote = db.Column(db.Integer, default=0, nullable=False)
    right_vote = db.Column(db.Integer, default=0, nullable=False)
    def __repr__(self):
        return f'<Board {self.name}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))