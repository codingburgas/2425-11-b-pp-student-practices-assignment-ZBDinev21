from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime)

class SurveyForm(FlaskForm):
    q1 = IntegerField('Little interest or pleasure in doing things', validators=[DataRequired(), NumberRange(min=0, max=3)])
    q2 = IntegerField('Feeling down, depressed, or hopeless', validators=[DataRequired(), NumberRange(min=0, max=3)])
    q3 = IntegerField('Trouble sleeping or sleeping too much', validators=[DataRequired(), NumberRange(min=0, max=3)])
    q4 = IntegerField('Feeling tired or having little energy', validators=[DataRequired(), NumberRange(min=0, max=3)])
    q5 = IntegerField('Poor appetite or overeating', validators=[DataRequired(), NumberRange(min=0, max=3)])
    submit = SubmitField('Submit Survey')

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    responses = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime)

    user = db.relationship('User', backref=db.backref('surveys', lazy=True))