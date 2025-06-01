# Mental Health Survey Classifier

This is a student-made web application that predicts potential signs of depression or anxiety based on survey responses. The model uses logistic regression and is integrated into a Flask web app.

## 🚀 Features
- Custom-built logistic regression (no sklearn)
- Survey based on PHQ-9 (subset)
- User authentication with roles (user/admin)
- Admin dashboard to view/delete users
- Predictions based on survey inputs

## 📦 Tech Stack
- Python + Flask
- Flask-WTF, Flask-Login, Flask-Mail, Flask-Migrate
- Bootstrap 5 for styling
- pyodbc for MSSQL connection
- NumPy, joblib (for model handling)

## 📋 Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```

## 🛠️ Setup Instructions
1. Clone the repo:
```bash
git clone https://github.com/codingburgas/2425-11-b-pp-student-practices-assignment-ZBDinev21.git
cd 2425-11-b-pp-student-practices-assignment-ZBDinev21
```
2. Edit the `config.py` with your DB credentials.
3. Run the app:
```bash
python run.py
```

## 🧠 AI Model
The logistic regression is implemented manually and trained using PHQ-9-style numeric data. It returns binary predictions (1 = likely symptoms, 0 = low symptoms).

## 🧪 Testing
Basic unit tests are in `tests/`. To run:
```bash
python -m unittest discover tests/
```

## 📈 Roles
- **User**: can take the survey, view results
- **Admin**: can manage users, view database entries

## 📬 Email Confirmation
Flask-Mail + itsdangerous is used for user registration confirmation (optional).

## 📄 License
Student Project – Not for commercial or clinical use.
