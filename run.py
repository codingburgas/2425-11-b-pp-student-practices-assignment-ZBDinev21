

from app import create_app

app = create_app()
app.secret_key = 'your_secret_key'  # Secret key for session management

if __name__ == '__main__':
    app.run(debug=True)