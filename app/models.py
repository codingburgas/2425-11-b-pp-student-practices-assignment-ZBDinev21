from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'  # optional, to be explicit
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime)

    def __repr__(self):
        return f"<User {self.username}>"


class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    responses = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(100))
    shared = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime, nullable=False)

    user = db.relationship('User', backref=db.backref('surveys', lazy=True))

    def __repr__(self):
        return f"<SurveyResponse {self.id} by User {self.user_id}>"
