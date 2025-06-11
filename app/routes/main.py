from flask import Blueprint, flash
from flask_login import login_required, current_user
from app.forms import SurveyForm
from app.models import SurveyResponse
from app.extensions import db
import numpy as np
import json
from ai.logistic_custom import LogisticRegressionCustom as LogisticRegression

main_bp = Blueprint('main', __name__, template_folder='templates')

# Example: Load or initialize your trained model here
model = LogisticRegression()
model.coef_ = np.array([[0.3]*5])
model.intercept_ = np.array([-2.0])
model.classes_ = np.array([0, 1])

@main_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = SurveyForm()
    prediction = None

    if form.validate_on_submit():
        try:
            answers = [form.q1.data, form.q2.data, form.q3.data, form.q4.data, form.q5.data]
            score = np.array(answers).reshape(1, -1)
            result = model.predict(score)[0]
            prediction = 'Possible signs of depression' if result == 1 else 'No signs detected'

            survey = SurveyResponse(
                user_id=current_user.id,
                responses=json.dumps(answers),
                prediction=prediction,
                shared=False
            )
            db.session.add(survey)
            db.session.commit()
            flash('Survey submitted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the survey.', 'danger')