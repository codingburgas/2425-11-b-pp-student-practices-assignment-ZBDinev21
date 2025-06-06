from flask import Blueprint, render_template, flash, session
from app.forms import SurveyForm
from app.models import SurveyResponse
from app.extensions import db
import numpy as np
from ai.logistic_custom import LogisticRegressionCustom as LogisticRegression

main_bp = Blueprint('main', __name__, url_prefix='/main')
# Dummy model setup
model = LogisticRegression()
model.coef_ = np.array([[0.3]*5])
model.intercept_ = np.array([-2.0])
model.classes_ = np.array([0, 1])

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    prediction = None

    if form.validate_on_submit():
        answers = [form.q1.data, form.q2.data, form.q3.data, form.q4.data, form.q5.data]
        score = np.array(answers).reshape(1, -1)
        result = model.predict(score)[0]
        prediction = 'Possible signs of depression' if result == 1 else 'No signs detected'

        survey = SurveyResponse(
            user_id=session.get('user_id'),
            responses=str(answers),
            prediction=prediction,
            shared=False
        )
        db.session.add(survey)
        db.session.commit()
        flash('Survey submitted.', 'success')

    return render_template('survey.html', form=form, prediction=prediction)