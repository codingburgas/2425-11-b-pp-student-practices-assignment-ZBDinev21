class Config:
    DRIVER = "ODBC Driver 17 for SQL Server"

    SERVER = "GL024\\SQLEXPRESS"

    DATABASE = "projectJune"

    SQLALCHEMY_DATABASE_URI = "sqlite:///projectJune.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'your_secret_key'