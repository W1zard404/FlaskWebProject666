from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    db.create_all()
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')  # Corrected variable name

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return render_template('registration.html', message="Пользователь уже существует!")

    if password != confirm_password:
        return render_template('registration.html', message="Пароли не совпадают!")

    password_hash = generate_password_hash(password)
    new_user = User(email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return redirect(url_for('index'))

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    PORT = int(os.environ.get('SERVER_PORT', '5555'))
    app.run(host=HOST, port=PORT)