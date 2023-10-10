from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import secrets

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Danil2002@localhost/prelev'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Модель для таблицы пользователей
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    salt = db.Column(db.String(120), nullable=False)

# Генерируем уникальную соль для каждого пользователя
salt = secrets.token_hex(16)

@app.route('/')
def index():
    return 'Добро пожаловать на главную страницу!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        plain_password = request.form['password']  # Получаем пароль в чистом виде
        email = request.form['email']

        # Хэшируем пароль с использованием Bcrypt и уникальной соли
        hashed_password = bcrypt.generate_password_hash(salt + plain_password).decode('utf-8')

        # Проверка, существует ли пользователь с таким же именем пользователя или email
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()

        if existing_user:
            flash('Пользователь с таким именем пользователя или email уже существует', 'danger')
        else:
            # Если пользователь не существует, выполняем регистрацию
            new_user = User(username=username, password=hashed_password, email=email, salt=salt)
            db.session.add(new_user)
            db.session.commit()

            flash('Регистрация успешно завершена!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        plain_password = request.form['password']  # Получаем пароль в чистом виде

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, salt + plain_password):  # Сравниваем хэш пароля с солью
            # Пользователь успешно аутентифицирован
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('index'))
        else:
            # Аутентификация не удалась
            flash('Неверное имя пользователя или пароль', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
