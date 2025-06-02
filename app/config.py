from flask_sqlalchemy import SQLAlchemy
import urllib

db_config = SQLAlchemy()
db = db_config
class Config:
    DRIVER = "ODBC Driver 17 for SQL Server"

    SERVER = "GL024\\SQLEXPRESS"

    DATABASE = "projectJune"

    SQLALCHEMY_DATABASE_URI = (

        "mssql+pyodbc://@{server}/{db}?driver={driver}&trusted_connection=yes"

        .format(

            server=SERVER,

            db=DATABASE,

            driver=urllib.parse.quote_plus(DRIVER)

        )

    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'your_secret_key'