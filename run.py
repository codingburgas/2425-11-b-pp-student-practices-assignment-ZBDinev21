from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuration
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your_email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your_app_password')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'your_email@gmail.com')

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer)
    role = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    survey_results = db.relationship('SurveyResult', backref='user', lazy=True)


class SurveyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.Column(db.JSON)
    score = db.Column(db.Integer)


# Create tables
with app.app_context():
    db.create_all()


# Helper function for sending emails
def send_email(recipient, subject, template, **kwargs):
    try:
        msg = Message(
            subject,
            recipients=[recipient],
            html=render_template(f'emails/{template}', **kwargs)
        )
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email to {recipient}: {str(e)}")
        return False


# Routes
@app.route('/')
def home():
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()
        return render_template('home.html', user=user)
    return render_template('home.html')


@app.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if 'user' not in session:
        flash('Please login to take the survey', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        answers = {}
        for i in range(1, 16):
            answer = request.form.get(f'q{i}')
            if answer is None:
                flash('Please answer all questions', 'error')
                return redirect(url_for('survey'))
            answers[f'q{i}'] = answer

        try:
            score = sum(int(val) for val in answers.values())
        except ValueError:
            flash('Invalid answer format', 'error')
            return redirect(url_for('survey'))

        user = User.query.filter_by(username=session['user']).first()
        survey_result = SurveyResult(user_id=user.id, answers=answers, score=score)
        db.session.add(survey_result)
        db.session.commit()

        # Send survey results email
        if user.email:
            send_email(
                user.email,
                "Your MH Classifier Survey Results",
                "survey_results.html",
                username=user.username,
                score=score,
                results_url=url_for('view_results', _external=True)
            )

        session['survey_results'] = answers
        session['survey_score'] = score
        return redirect(url_for('view_results'))

    return render_template('survey.html')


@app.route('/view_results')
def view_results():
    if 'user' not in session:
        flash('Please login to view results', 'error')
        return redirect(url_for('login'))

    if 'survey_results' not in session:
        flash("No survey results found. Please complete the survey first.")
        return redirect(url_for('survey'))

    results = session['survey_results']
    score = session['survey_score']
    return render_template('view_results.html', results=results, score=score)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        flash('Please login to edit profile', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['user']).first()

    if request.method == 'POST':
        new_email = request.form.get('email')

        # Check if email is being changed and if it's already taken
        if new_email and new_email != user.email:
            if User.query.filter_by(email=new_email).first():
                flash("Email already in use by another account", 'error')
                return redirect(url_for('edit_profile'))
            user.email = new_email

        user.age = request.form.get('age')
        user.role = request.form.get('role')
        user.gender = request.form.get('gender')
        db.session.commit()
        flash("Profile updated successfully.")
        return redirect(url_for('home'))

    return render_template('edit_profile.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mode = request.form.get('mode')
        username = request.form['username']
        password = request.form['password']

        if mode == 'register':
            if User.query.filter_by(username=username).first():
                flash("Username already exists. Please log in instead.")
                return redirect(url_for('login'))

            email = request.form.get('email')
            if email and User.query.filter_by(email=email).first():
                flash("Email already in use. Please use another email or log in.")
                return redirect(url_for('login'))

            hashed_password = generate_password_hash(password)
            user = User(
                username=username,
                email=email,
                password=hashed_password,
                age=request.form.get('age'),
                role=request.form.get('role'),
                gender=request.form.get('gender')
            )
            db.session.add(user)
            db.session.commit()

            # Send welcome email
            if email:
                send_email(
                    email,
                    "Welcome to MH Classifier",
                    "welcome.html",
                    username=username,
                    dashboard_url=url_for('home', _external=True)
                )

            session['user'] = username
            flash("Registration successful.")
            return redirect(url_for('home'))

        elif mode == 'login':
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user'] = username
                flash("Login successful.")
                return redirect(url_for('home'))
            else:
                flash("Invalid username or password.")
                return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)