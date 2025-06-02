from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

if __name__ == '__main__':
    app.run(debug=True)