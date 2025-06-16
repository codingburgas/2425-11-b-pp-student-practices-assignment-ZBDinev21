# Project Dependencies

## - Core Requirements

```text
Flask==2.3.2
Flask-WTF==1.1.1
Flask-SQLAlchemy==3.0.3
Flask-Login==0.6.2
Flask-Mail==0.9.1
Flask-Migrate==4.0.4
python-dotenv==1.0.0
```

## - Database

```text
SQLAlchemy==2.0.19
pyodbc==4.0.39          

## - Authentication & Security

```text
bcrypt==4.0.1
itsdangerous==2.1.2
email-validator==2.0.0
```

## - Machine Learning

```text
numpy==1.24.3
joblib==1.3.2
scikit-learn==1.3.0    
```

## - Frontend

```text
Flask-Bootstrap==3.3.7.1
```

## - Development & Testing

```text
pytest==7.4.0
Faker==19.3.0
```

## - Production (Optional)

```text
gunicorn==20.1.0        
```

---

## - Installation

```bash
pip install -r requirements.txt
```

---

## - Notes

- **SQLite**: Included in Python standard library (no additional package needed for development)
- **MSSQL**: Requires ODBC drivers installed on system
- **Email**: Requires proper SMTP server configuration
- **scikit-learn**: Only used for model comparison, not in production workflow
- **Bootstrap**: Used for frontend templates and styling

---

## - Development Setup

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.env\Scriptsctivate   # Windows
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## - Version Pinning

All packages are version-pinned to ensure consistent behavior across installations.
