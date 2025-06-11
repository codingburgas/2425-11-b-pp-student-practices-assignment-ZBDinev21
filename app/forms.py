from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SurveyForm(FlaskForm):
    q1 = IntegerField('Little interest or pleasure in doing things', validators=[DataRequired(), NumberRange(min=0, max=3)])
    q2 = IntegerField('Feeling down, depressed, or hopeless', validators=[DataRequired(), NumberRange(min=0, max=3)])
    q3 = IntegerField('Trouble sleeping or sleeping too much', validators=[DataRequired(), NumberRange(min=0, max=3)])
    q4 = IntegerField('Feeling tired or having little energy', validators=[DataRequired(), NumberRange(min=0, max=3)])
    q5 = IntegerField('Poor appetite or overeating', validators=[DataRequired(), NumberRange(min=0, max=3)])
    submit = SubmitField('Submit Survey')

