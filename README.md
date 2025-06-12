# Mental Health Survey Classifier

A Flask web application that predicts potential signs of depression or anxiety using custom logistic regression on PHQ-9-style survey responses, with user authentication and admin dashboard.

## 📌 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Running the App](#-running-the-app)
- [AI Model](#-ai-model)
- [Testing](#-testing)
- [Application Structure](#-application-structure)
- [License](#-license)

## 🚀 Features

### Machine Learning
- Custom logistic regression implementation (no sklearn)
- Trained on synthetic PHQ-9-style numeric data
- 9-question survey (0-3 scale per question)
- Binary prediction output (1 = likely symptoms, 0 = low symptoms)
- Model persistence with joblib

### User System
- Role-based authentication (user/admin)
- Secure password hashing with Flask-Bcrypt
- Email confirmation (optional)
- Profile management
- Password reset functionality

### Admin Dashboard
- User management (view/delete)
- Survey response analytics
- Database administration
- Role assignment

### Survey System
- PHQ-9 inspired questionnaire
- Results visualization with Chart.js
- Response history tracking
- Responsive design

## 📦 Tech Stack

**Backend:**
- Python 3.8+
- Flask
- Flask extensions: WTF, Login, Mail, Migrate, SQLAlchemy
- Custom logistic regression (NumPy)
- MSSQL/pyodbc or SQLite
- joblib (model persistence)

**Frontend:**
- Bootstrap 5
- Chart.js
- Jinja2 templating
- Vanilla JavaScript

**Security:**
- CSRF protection
- Password hashing
- Secure session management

## 📋 Installation

1. Clone the repository:
```bash
git clone https://github.com/codingburgas/2425-11-b-pp-student-practices-assignment-ZBDinev21.git
cd 2425-11-b-pp-student-practices-assignment-ZBDinev21
