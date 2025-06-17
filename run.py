from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# In-memory user list
user_profiles = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
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

        session['survey_results'] = answers
        session['survey_score'] = score
        return redirect(url_for('view_results'))

    return render_template('survey.html')

@app.route('/view_results')
def view_results():
    if 'survey_results' not in session:
        flash("No survey results found. Please complete the survey first.")
        return redirect(url_for('survey'))

    results = session['survey_results']
    score = session['survey_score']
    return render_template('view_results.html', results=results, score=score)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        flash("Profile updated (not saved permanently - demo only).")
        return redirect(url_for('home'))
    return render_template('edit_profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mode = request.form.get('mode')
        username = request.form['username']
        password = request.form['password']

        if mode == 'register':
            if any(u['username'] == username for u in user_profiles):
                flash("Username already exists. Please log in instead.")
                return redirect(url_for('login'))

            profile = {
                'username': username,
                'password': password,
                'email': request.form.get('email'),
                'age': request.form.get('age'),
                'role': request.form.get('role'),
                'gender': request.form.get('gender')
            }
            user_profiles.append(profile)
            session['user'] = username
            flash("Registration successful.")
            return redirect(url_for('home'))

        elif mode == 'login':
            user = next((u for u in user_profiles if u['username'] == username and u['password'] == password), None)
            if user:
                session['user'] = username
                flash("Login successful.")
                return redirect(url_for('home'))
            else:
                flash("Invalid username or password.")
                return redirect(url_for('login'))

    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
