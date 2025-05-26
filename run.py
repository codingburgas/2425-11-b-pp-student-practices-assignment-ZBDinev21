import pyodbc
import bcrypt
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session, flash
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load DB config from a separate file
from config import db_config


# Custom Perceptron for binary classification
class Perceptron:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iterations):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_predicted = self.step_function(linear_output)
                update = self.learning_rate * (y[idx] - y_predicted)
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        return self.step_function(linear_output)

    def step_function(self, x):
        return np.where(x >= 0, 1, 0)


# Instantiate models
linear_reg = LinearRegression()
perceptron = Perceptron()
scaler = StandardScaler()

# Example data for demo model training
X_train = np.array([[1], [2], [3], [4], [5]])
y_lin_train = np.array([2, 4, 6, 8, 10])      # Linear relationship
y_perc_train = np.array([0, 0, 1, 1, 1])      # Binary classification

# Train models
linear_reg.fit(X_train, y_lin_train)
X_scaled = scaler.fit_transform(X_train)
perceptron.fit(X_scaled, y_perc_train)


# Database connection helper
def get_db_connection():
    connection_string = (
        f"DRIVER={db_config['driver']};"
        f"SERVER={db_config['server']};"
        f"PORT=1433;"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['username']};"
        f"PWD={db_config['password']}"
    )
    return pyodbc.connect(connection_string)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash('Welcome back!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect login credentials.', 'danger')
        except Exception as e:
            app.logger.error(f"Login error: {e}")
            flash("Something went wrong. Please try again.", 'danger')
        finally:
            if 'conn' in locals() and conn:
                conn.close()
    return render_template('login.html')


@app.route('/submit_survey', methods=['GET', 'POST'])
def submit_survey():
    prediction = None
    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            prediction = linear_reg.predict([[value]])[0]
        except ValueError:
            flash('Enter a valid number.', 'danger')

    return render_template('linear_predict.html', prediction=prediction)


@app.route('/view_results', methods=['GET', 'POST'])
def view_results():
    prediction = None
    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            scaled_value = scaler.transform([[value]])
            pred = perceptron.predict(scaled_value)[0]
            prediction = "You may be experiencing symptoms." if pred == 1 else "Results appear within typical range."
        except ValueError:
            flash('Please enter a valid number.', 'danger')

    return render_template('perceptron_predict.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
