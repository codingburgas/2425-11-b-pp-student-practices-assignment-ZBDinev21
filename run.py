from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # e.g., answers = request.form.to_dict()
        return redirect(url_for('home'))
    return render_template('survey.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('edit_profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)


